---
title: Rtl-Sdr ile GSM Ağında Sinyal Analizi
comments: true
layout: post
date: '2019-08-11 12:00:00'
author: furkan önder
categories:
- rtl-sdr
- GSM
tags:
- Rtl-Sdr ile GSM
description: rtl-sdr kullanarak GSM ağında sinyal analizi
---

Selamlar,

Rtl-sdr ile uğraşırken sinyal aralağının çok geniş olduğu aklıma geldi.500kHz ile 1.75 GHz frekans aralağını dinleyebiliyorsunuz.Sonra cep telefonlarınımızda kullandığımız GSM teknolojisinin bu frekans aralığına girebileceğini düşündüm ve giriyormuş :) Biraz araştırma yaptıktan sonra bu konuda yapılmış çalışmalara göz attım.Öğrendiklerimi ve tecrübelerimi bu yazıda yazmaya karar verdim.

Rtl-sdr ne derseniz, sdr kelimesinin açılımı “Software Defined Radio” (yazılım tabanlı radyo).Yazılımla kolayca kontrol edilebilmesi ve geniş bir frekans aralığına sahip olduğu için kullanışlı olmasından dolayı çok popüler.Fm radyo dinleyebiliyorsunuz,üzerinizden geçen uydulardan sinyal alabiliyorsunuz, TV yayını alabiliyorsunuz ve daha bir çok amaç için kullanabiliyorsunuz.

## Gelelim GSM’e
GSM ağına rtl-sdr ile nasıl dahil olabiliriz,sinyal alabiliriz? [Gimp](https://www.gimp.org/) ile işe güzel bir çizim yaparak anlatmayı düşündüm :)

<a href="/assets/images/gsm/baz.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 33em;" src="/assets/images/gsm/baz.png"/>
</a>

Kırmızı ve mavi olan kuleler  çevremizdeki gerçek baz istasyonlarımız olsun. Mor olan kutumuz ise rtl-sdr ile yaptığımız sahte baz istayonumuz olsun.Yakınımızdaki cep telefonlarına kendimizi baz istasyonu olarak tanıtıp onlardan veri alacağız.

## Nelere ihtiyacımız var?
<a href="/assets/images/gsm/rtl-sdr.jpg" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 33em;height:500px;width:500px;" src="/assets/images/gsm/rtl-sdr.jpg"/>
</a>

### Donanım
* Rtl-Sdr 

Yukarıda resimde kullandığım rtl-sdr ‘a görüyorsunuz.RTL2832u entegresine sahip herhangi bir rtl-sdr kullabilirsiniz.Yurt içindeki ve dışındaki internet siteleri üzerinde satılıyor.

### Yazılım
* [Wireshark](https://www.wireshark.org/) – Paketlerimizi incelemek için kullanacağız.
* [Gr-gsm](https://github.com/ptrkrysik/gr-gsm) – Sinyallerimizi yakalamak için kullancağız.
* [kalibrate-rtl](https://github.com/steve-m/kalibrate-rtl) – Rtl-sdr’ın kalibrasyonunu için kullanacağız.
* [IMSI-catcher]( https://github.com/Oros42/IMSI-catcher) –  IMSI verilerini bize gösteren bir python betiği.
* Gnu/Linux tabanlı bir işletim sistemi(Windows üzerinde bu işlemler yapılabiliyor ama ben bütün denemeleri Gnu/Linux tabanlı bir işletim sisteminde denedim)


## Hadi Başlayalım 
Öncelikle işe rtl-sdr’imızın kalibrasyonu yapmak ile başlıyoruz.
```
kal -s GSM900 -g 40
```
komutunu çalıştırıyoruz.

GSM standardında ihtiyaca göre frekans aralıklarına bölünmüş GSM için radyo frekansları vardır.GSM900 bunlardan en yaygını olan olduğu için ilk parametremiz bu olacak. Yapacağımız aramanın dbi aralığını ise 40 olarak olarak ayarladık.   
 
<a href="/assets/images/gsm/kal.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 33em;" src="/assets/images/gsm/kal.png"/>
</a>

Farklı kanal ve frekans aralıklarına kullanan bir çok bilgiye sahibiz.Bu bilgileri elde ettiğimize göre artık paket almaya başlayabiliriz.

```
gr_gsm livemon
```
komutunu çalıştırıyoruz.
Sağ tarafta frequency bölümene gelip daha önce kalibre ettiğimizde elde ettiğimiz frekanslardan birini yazıyoruz.Sol kısımdaki gibi gelen verileri görüyorsanız doğru yoldasınız demektir.

<a href="/assets/images/gsm/grgsm.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 33em;" src="/assets/images/gsm/grgsm.png"/>
</a>

Şimdi gelen verilerimizi analiz etmek için wireshark aracımızı açıyoruz.Capture bölümden Loopback:lo ‘yu seçiyoruz.

Ben Wireshark’ı çalıştırdığımda LAPDm ve GSMTAP şeklinde 2 protokol üzerinden veri aldım.LAPDm, GSM şebekelerinde kullanılan bir veri bağlantı katmanı protokolüdür. Hücresel şebeke ile abone arasındaki telsiz bağlantısında kullanılıyor.GSMTAP ise wireshark tarafından kullanan GSM  arayüzünden çerçeveler taşımak için kullanılan sahte bir başlık.

Protokoller üzerinden elde ettiğim paket başlıkları;

GSMTAP:
  * Paging Request Type 1,2,3,4
  * System Information Type 3,4,13,2quarter
  * Immediate Assingment

LAPDm:
  * System Information Type 5,6
  * Authentication Request
  * Ciphering Mode Command 
  * Identity Request 


## Gelelim paketleri incelemeye....
GSMTAP protokolü System Information Type 4 paketini inceliğimizde Local Area Identification( Konum Alanı Kimliği) kısmı gözümü çarpıyor.

Local Area Identification (Konum Alanı Kimliği), bir mobil ağ içindeki bir konum alanını (LA) benzersiz şekilde tanımlar. Mobil Ülke Kodu (MCC), Mobil Şebeke Kodu (MNC) ve Konum Alan Kodu'ndan (LAC) oluşur. LAI, ağdaki mobil aboneleri takip etmek için kullanılır. Bu kayıt, GSM şebekesindeki Visitor Location Register  (Ziyaretçi Yer Kaydı)  gibi bir veri tabanında tutuluyor.

<a href="/assets/images/gsm/lai.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 33em;" src="/assets/images/gsm/lai.png"/>
</a>

Yukarıda resimde bunları görebiliyoruz. MCC kodu Türkiye için 286, MNC kodu ise GSM  operatörlerin ülke içerisinde kullandığı kod,örneğin Turkcell için 01.LAC kodu ise GSM operatörünün verdiği Konum Alanı Kimliği.

<a href="/assets/images/gsm/encrpytion.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 33em;" src="/assets/images/gsm/encrpytion.png"/>
</a>

GSMTAP protokolü  üzerinde Ciphering Mode Command Identification kısmını  görüyoruz.Tahmin ettiğimiz gibi GSM üzerindeki haberleşmemizi güvenli kılan yapılardan biri.A5/3 algorithması kullanılarak verilerimiz şifreleniyor.Hemen aklınıza gelebilir bu şifrelemeyi çözebilirmiyiz? Internet üzerinde şifrelemeyi çözmeyi gösteren video ve yazılar var.

<b>Not:</b> A5/3 algorithması kırmayı denediğiniz takdirde olacaklardan sorumlu değilim.Bu yazıdaki amacım GSM teknolojisinin hakkında biraz bilgi edinmek.

## IMSI Catcher(Yakalayıcı)
International Mobile Subscriber Identity (Uluslararası mobil abone kimliği) hücresel bir ağın her kullanıcısını benzersiz şekilde tanımlayan bir sayıdır. Gizli dinleyicilerin telsiz arabirimindeki aboneyi tanımlamasını ve izlemesini önlemek için IMSI nadiren gönderiliyor ve bunun yerine rastgele oluşturulmuş bir TMSI gönderiliyor.

[IMSI-catcher](https://github.com/Oros42/IMSI-catcher) içerisinde bulunan  simple_IMSI-catcher.py betiğini çalıştıralım.

<a href="/assets/images/gsm/imsi.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 33em;" src="/assets/images/gsm/imsi.png"/>
</a>

Bu betik işimizi kolaylaştırıyor Wireshark’ da paketleri tek tek incelemek yerine bu betiği kullanarak kolayca bilgi edinebiliyoruz. MMC,NNC ve LAC kavramlarının anlamlarından bahsetmiştim.Buna ek olarak burada Ülke,GSM operatörü adı,CellId, IMSI ve TMSI bilgilerini de görüyoruz.

IMSI ise şöyle elde ediliyor;

* İlk 3 rakam: 
Mobil Calling Code(Mobil Ülke Kodu),Türkiye için 286.

* Ortaki 2 rakam: 
Mobil Network Code (Mobil Şebeke Kodu), GSM operatörlerin ülke içerisinde kullandığı kod,örneğin Turkcell için 01.

* Son 10 rakam:
Mobile identification number (Mobil Tanımlama Kodu),GSM operatörünün kendisinin belirlediği bir değer.

Biraz uzun bir yazı oldu.Umarım hoşunuza gitmiştir.İyi çalışmalar.

## Referanslar
* https://en.wikipedia.org/wiki/GSM
* https://en.wikipedia.org/wiki/International_mobile_subscriber_identity
* https://en.wikipedia.org/wiki/IMSI-catcher