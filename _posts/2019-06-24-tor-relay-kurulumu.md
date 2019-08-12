---
title: Tor Relay Kurulumu
comments: true
layout: post
date: '2019-06-24 00:30:00'
author: furkan önder
categories:
- tor
tags:
- Tor Relay Kurulumu
- tor relay nasıl kurulur
description: Tor ağında bir relay kurulumu
---

Merhaba,
Önceki yazımda Tor’un yapısında bulanan Onion Routing’in nasıl çalıştığı ile ilgili bir yazı yazmıştım.Şimdi ise merak edenler olabilceğini düşündüğüm için bir Tor ağında bir relay kurulumunun nasıl olacağını anlatacağım.Bu yazıda middle(ortanca) relay kuracağız.

# Peki nerede kurabiliriz?
[Burada](https://trac.torproject.org/projects/tor/wiki/TorRelayGuide#ASlocationdiversity) Tor’un relay kurlum rehberinde belirttiği üzere;
- OVH SAS (AS16276)
- Online S.a.s. (AS12876)
- Hetzner Online GmbH (AS24940)
- DigitalOcean, LLC (AS14061)

firmalarını tavsiye __etmeMEmizi__ istiyor.Çünkü bu firmalarda çok fazla Tor relay’ı bulunmaktadır.Peki hangi firmaları tercih edebiliriz derseniz, Tor’un rehberindeki [detailed list of all the Tor-friendly hosting providers](ttps://trac.torproject.org/projects/tor/wiki/doc/GoodBadISPs)
kısmından öğrenebilirsiniz.

# Kurulum
Ben kurulumumu Centos tipi bir sunucu üzerinde yapacağım.Başka tip Linux/Windows sunucularda da kurabilirsiniz. İnternet, interneti tarayan ve sunucuların kontrolünü ele almaya çalışan botlarla doludur.Relay kurulumuna geçmeden önce sunucumuzun güvenliğini artıralım.

# SSH Anahtarlarının ayarlanması
Sunucuza bağlandığın zaman bir çok başarız ssh oturum girişimi olduğunu görmüşsünüz.Yukarıda belirtiğim gibi bunun nedeni bir çok deneme yapılarak sunucunuza girilmek istenilmesidir.Bunun önüne geçelim.

Sunucumuzdaki komut satırımıza
```
ssh-keygen -t rsa
```
yazarak anahtarlarımızı oluşturalım.

Kendi bilgisayarımıza gelelip keylerimizi alalım:

```
ssh-copy-id kullanıcı-adınız@sunucu-ip-adresiniz
```

Ve son olarak sunumucuza gelip şifreli ssh bağlantıları kapatalım.Ben dosyalarımı düzenlerken favori editörüm olan vim ile düzenliyorum.Vim yerine nano,vi vb editörlerde kullanabilirsiniz.

```
sudo vim /etc/ssh/sshd_config
```
'''
PasswordAuthentication no
'''
şeklinde satırımızı düzenleyelim.

SSH servisimizi tekrar başlatalım.
```
sudo systemctl restart sshd.service
```

# Iptables Kurulumu
Sunucumuzda terminale
```
sudo yum install iptables-services
```
yazarak iptables paketini kuralım.Iptables’ımızı yapılandırmaya geçelim.

Sunucunuz tarafından oluşturulan trafiğe izin verelim.
```
iptables -A INPUT -i lo -j ACCEPT
```

SSH port 22 bağlantılarını kabul edelim. Çok önemlidir, aksi takdirde sunucumuza bağlanamayız.
```
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

Tor 9001 ORPort portunu  kullanarak internete bağlanıyor.Buna izin verilim.
```
iptables -A INPUT -p tcp --dport 9001 -j ACCEPT
```

Bu isteğe bağlı.Tor'un relaylarının birbirleriyle senkronize olmasına yardımcı olmak için kullanır.İzin verdiğiniz takdirde herhangi bir zararı olmaz.
```
iptables -A INPUT -p tcp --dport 9030 -j ACCEPT
```
ICMP'ye izin verelim
```
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 2/s -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
iptables -A INPUT -p icmp -j ACCEPT
```
Engellenen trafikleri kayıt edelim.
```
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7
```

Diğer tüm trafiği engelleyelim.
```
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -m state --state INVALID -j DROP
```

Kurallarımızı kaydedelim.
```
iptables-save
```

Iptables'ımızı başlatalım.

```
systemctl start iptables
```

Son olarak iptables'ı sunucu açıldığında otomatik olarak başlayacak şekilde etkinleştirelim.
```
systemctl enable iptables
```

# Relay'ın Yapılandırılması
Sunucumuzda terminale

```
yum install epel-release
yum install tor
```

yazarak tor paketini kuralım.Şimdi terminalimize gelip
```
vim /etc/tor/torrc 
```
yazarak relayımızı yapılandırmaya başlayalım.<br>

SOCKSPort, yalnızca yerel uygulamalara bağlantı yapmak için relay’ı kullanıyorsanız gereklidir. Bu kurulum  için gerekli olmadığı için 0 olarak ayarlıyoruz.
```
SOCKSPort 0
```

Relay’ın arkaplanda bir daemon olarak çalışmasını istediğimiz için 1 olarak ayarlıyoruz.
```
RunAsDaemon 1 
```

Relay 9001 ORPort portunu kullanarak internete bağlanıyor.Buna izin verilim.
```
ORPort 9001
```

DirPort’u Tor'un relaylarının birbirleriyle senkronize olmasına yardımcı olmak için kullanır.Bunu 9030  
olarak ayarlıyoruz.
```
DirPort 9030
```

Bir exit(çıkış) relayı kurmak istemediğimiz için aşağıdaki şekilde  ayarlıyoruz.
```
ExitPolicy reject *:* 
```

Loglamayı aktif hale getirelim.
```
Log notice file /var/log/tor/notices.log
```

Relay’ın kullanacağı toplam trafik miktarını ayarlayalım.Bunu ben seçtiğiniz firmanın size aylık 1TB trarfik verdiğini varsayarak ayarladım.Bunu kendinize göre ayarlabilirsiniz. 
```
AccountingMax 999 GBytes
```

Trafik sayacının ne zaman başlayacağını ayarlayalım.
```
AccountingStart month 1 15:00 
```

Relay’ımıza bir isim verelim
```
Nickname RelayAdı
```

Relay’ımıza iletişim bilgisi ekleyelim. Relay’ımızda herhangi sorun olduğu zaman Tor size bir mail yollamak için kullanır.
```
ContactInfo herkimse email[at]email[dot]com
```

değişikliklerimizi yaptıktan sonra dosyamızı kaydedelim.

Tor relay'ımızı başlatalım.
```
systemctl restart tor
```
Son olarak tor'u sunucu açıldığında otomatik olarak başlayacak şekilde etkinleştirelim
```
systemctl enable tor
```

# Relay durumu
Kurulumumuzu bitirdiğimize göre relay’ın sağlıklı çalıştığından emin olalım.
```
cat /var/log/tor/notices.log 
```
yazdığımızda;
<a href="/assets/images/relay.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;height:50px;width:1090px;" src="/assets/images/relay.png"/>
</a>
şeklinde bir yazı ile karşılaşmamış gerekiyor.Ek olarak [buradan](https://metrics.torproject.org/rs.html#search/) relay'ımızın adını aratarak bilgi edinebiliriz.