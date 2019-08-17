---
title: Python ile SQLite’a Giriş
comments: true
layout: post
date: '2018-08-04 01:30:00'
author: furkan önder
categories:
- Python
tags:
- Python ile SQLite’a Giriş
description: Python ile SQLite kullanımı
---

Merhaba,
Bu yazımızda Python’da Veritabanı Programlama’ya bir giriş yapıcağız.Bunun için Dolar/Tl kurundaki alış ,satış değerlerini ve bu değerleri elde ettiğimiz tarih ve saati veritabanına kaydeden küçük bir bot yazacağız.Veritabanını, içinde bilgi saklanabilen,birbiriyle ilişkili olan verilerin tutulduğu, yönetilebilir, güncellenebilir ve taşınabilir bilgi topluluğu olarak adlandırabiliriz.

## SQLite Ve Python
SQLite, python programlama dilinde varsayılan olarak gelen bir veritabanıdır. Django ve Flask gibi python ile yazılan Web Frameworklerde de  varsayılan olarak SQLite gelmektedir.SQLite, diğer veritabanlarına göre kolay bir yapıya sahiptir.

## Veritabanımızı Oluşturalım
Öncelikle sqlite3 kütüphanesini kodumuza dahil edelim.

```
import sqlite 
```

Veritabanımızı connect() methodu ile oluşturalım.

```
vt = sqlite3.connect('kur.db') 
```

Veritabanı üzerinde işlem yapabilmek bir imleçe ihtiyaç duyarız. cursor() methodu ile imlecimizi oluşturalım.

```
imlec = vt.cursor() 
```

Tablo oluşturmak için execute methodunu kullanıyoruz.kurTablosu adında bir tablo oluşturalım.Integer türünde sira ;varchar türünde alis, satis ve zaman değerlerine sahip olsun.Sira değişkenine  AUTOINCREMENT özelliği ekleyerek veritabanına veriler eklendikçe sıra değişkeninin artmasını sağlayalım.

```
imlec.execute('''
    CREATE TABLE kurTablosu(
    sira INTEGER PRIMARY KEY AUTOINCREMENT,
    alis VARCHAR,
    satis VARCHAR,
    zaman VARCHAR )''')
```

Verilerimizi veritabanına commit metodu ile işleyelim.

```
vt.commit() 
```

close() metodu ile veritabanı bağlantımızı kapatalım.

```
vt.close() 
```

## Veritabanı İçin Verilerin Elde Edilmesi
Veritabanına eklemek için Dolar/Tl kurundaki alış ,satış değerlerini elde etmemiz gerekiyor.
Bunu kullanımımıza sunulan bir API ile kolayca yapabiliriz.API, Application Programming Interface(Uygulama Programlama Arayüzü) kelimelerinin baş harflerinden oluşan bir kısaltmadır.API’ı bir uygulamaya ait işlevlerin başka bir uygulamada kullanılmış bir arayüz olarak tanımlayabiliriz.
(API hakkında daha fazla bilgi edinmek için <a href="http://www.wiki-zero.co/index.php?q=aHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvQXBwbGljYXRpb25fcHJvZ3JhbW1pbmdfaW50ZXJmYWNl" target="_blank"> burayı</a> ziyaret edebilirsiniz.)

Dolar/TL kurundaki alış ve satış değerlerini elde etmek için dolar adında bir fonksiyon yazalım.

```
def dolar():
    url = 'https://www.doviz.com/api/v1/currencies/USD/latest'
    istek = urllib.request.Request(url)
    i = urllib.request.urlopen(istek).read()
    veri = json.loads(i.decode('utf-8'))

    return veri['buying'], veri['selling']
```

API adresimizi url değişkenine atadık.Request fonksiyonu ile url ‘e bir istek yolladık.urlopen() fonksiyonu ile isteği açtık ve read() fonksiyonu ile okuduk.Okuduğumuz bu isteği  utf-8 türünde çözümleyip json şekline dönüştürdük.Ve son olarak  veri['buying'], veri['selling'] şeklinde alış ve satış değerlerini elde ettik ve bu iki değeri döndürdük.

# Veritabanına Verilerin Eklenmesi
Dolar() fonksiyonunu kullanarak verilerimizi elde etmiştik.Şimdi ise bu verileri veritabanına eklemeliyiz.Bunun için ise vtEkle fonksiyonu yazalım.

Fonksiyonumuz 3 parametre alsın.alis ,satis ve TarihVeSaat bilgisi.

```
def vtEkle(alis, satis, TarihVeSaat):
```

Daha önce oluşturduğumuz  kur.db veri tabanına bağlanalım.

```
vt = sqlite3.connect('kur.db')
```

Bir imleç oluşturalım.

```
imlec = vt.cursor()
```

Tablomuza verileri eklemek için bir SQL sorgusu yazmamız gerekiyor.Bunun için bir sorgu yazalım ve execute metodu ile çalıştıralım.(SQL hakkında daha fazla bilgi edinmek için <a href="https://www.w3schools.com/sql/" target="_blank"> burayı</a> ziyaret edebilirsiniz.)

```
imlec.execute("INSERT INTO kurTablosu (alis,satis,zaman) VALUES(?,?,?)", (alis, satis, TarihVeSaat))
```

Verilerimizi veritabanına commit metodu ile işleyelim.

```
vt.commit()
```

close() metodu ile veritabanı bağlantımızı kapatalım.

```
vt.close()
```

## Neredeyse Bitti!

Kodumuz tamamlanmak üzere küçük bir eksiğimiz var.Veri tabanımıza belli aralıklarla Dolar/Tl kurundaki alış,satış,tarih ve saat bilgilerini veri tabanına eklememiz gerekiyor.

```
while True:
    alis, satis = dolar()
    print("Alış:", alis, "Satış:", satis, "Tarih ve Saat:", datetime.datetime.now())
    vtEkle(str(alis), str(satis), str(datetime.datetime.now()))
    time.sleep(300)
```

Bir döngü oluşturduk. dolar() fonksiyonumuzu çağırdık ve dönen değerleri alis ve satis değişkenine atadık.Tarih ve Saat bilgisi için datetime modülünden yararlandık.Alış ,satış, Tarih ve Saat bilgilerini vtEkle() fonksiyonu gönderdik. time.sleep(300) ile her  5 dk da  bir veritabanına verilerimizi  ekledik.

## Veritabanındaki Verileri Okumak
Veritabanımıza eklediğimiz bilgileri okuyalım.Bunu linux komut satırından kolayca yapabiliriz.
Bunun için sqlite3 paketinin yüklü olması gerekiyor.

<a href="/assets/images/konsol.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;" src="/assets/images/konsol.png" />
</a>

Terminalimizi veri tabanımızın olduğu dizinde açalım.
Veritabanına girmek <b>sqlite3 kur.db</b> yazalım
<b>.tables</b> ile veritabanındaki tablo isimlerine bakalım.
<b>SELECT * FROM kurTablosu;</b> sql sorgusunu yazarak tablomuzu görelim.

Kodun tam hali görmek için <a href="https://github.com/furkanonder/furkanonder.github.io/tree/master/codes/dolarKuruSqlite.py/" target="_blank"> buraya </a>bakabilirsiniz.İyi çalışmalar dilerim.
