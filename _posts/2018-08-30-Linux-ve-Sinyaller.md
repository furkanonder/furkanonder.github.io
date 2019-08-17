---
title: Linux ve Sinyaller
comments: true
layout: post
date: '2018-08-30 01:30:00'
author: furkan önder
categories:
- Linux
- Sinyaller
tags:
- Linux ve Sinyaller
description: Linux'daki sinyal yapısının çalışma şekli
---

Merhaba,
Bu yazı da Linux işletim sisteminde yer alan sinyallerden bahsedeceğim.Sinyali kısaca tanımlamak gerekirse; bir prosese,proses tarafından ya da başka bir proses tarafından gönderilen mesaj olarak tanımlayabiliriz.Bu mesaja göre kapatma,durdurma ve başlatma gibi  sistemsel eylemler gerçekleşebilir.

Sistemimizde bulunan sinyalleri öğrenmek için terminale

``` 
kill -l 
```

komutunu yazalım.

<a href="/assets/images/sinyaller.png" imageanchor="1">
	<img style="display: block;margin: 0 auto;" src="/assets/images/sinyaller.png"/>
</a>

Resimde görüldüğü üzere sistemimizde 64 adet sinyal bulunuyor. Burada yer alan sinyaller
içerisinden Sonlandırma Sinyalleri’ni inceleyeceğiz.

## SIGINT
SIGINT sinyali,signal(sinyal) ve interrupt (kesmek) kelimelerinden türetilmiştir.Çalışan prosesleri iptal etmek için gönderirilir.Ctrl+C kombinasyonu klavyeden uygulanarak bu sinyal gönderilebilir.

## SIGTERM
SIGTERM sinyali,signal(sinyal) ve terminate (sona erdirmek) kelimelerinden türetilmiştir. Prosesin sona erdirilmesi için kullanılır.Bu sinyal prosesi sonlandırmak için bazen yetersiz kalabilir. Çünkü prosese gelen sinyal engellenebilir ya da yoksayılabilir. Bu gibi durumlarda ise SIGKILL sinyali gönderilir.

## SIGKILL
SIGKILL sinyali, bir prosese gönderildiğinde bu proses her zaman son bulur.Bu sinyal yakalanamaz ya da yok sayılamaz.

## Sinyal Göndermek
Sistemimizde çalışan  proseslere sinyal göndereceğiz.Çalışan prosesleri görmek için terminale

```
top
```

yazdık.

<a href="/assets/images/top.png" imageanchor="1">
	<img style="display: block;margin: 0 auto;"  src="/assets/images/top.png" />
</a>

Sistemde çalışan prosesleri görüyorsunuz.Listenin başına baktığımızda, en solunda prosesin PID değerini  sonunda ise çalışan prosesisin adı olan  firefox ‘u görüyorsunuz.Sinyal gönderirken PID değerini kullanacağız.Firefox prosesine bir kill sinyali gönderilim.Bunu 2 şekilde yapabiliriz.

<b>kill</b> <b>Sinyal adı</b> ve <b>PID değerini</b> yazarak sinyal gönderebiliriz.

``` 
kill -KILL 18229 
```

Başka bir  yöntem ise <b>kill</b> <b>sinyal numarası</b> ve <b>PID</b> değerini yazarak sinyal göndermektir.Yazımızın başında terminale kill-l yazarak sinyallari incelediğimizde, KILL sinyalinin numarasını 9 olarak görmüştük.

``` 
kill -9 18229 
```

## Sinyal Yakalamak
Sinyal göndermeyi öğrendiğimize göre sinyal yakalamayı da öğrenmeye başlayabiliriz.Sinyal yakalamak için bir bash scripti yazacağız.
Bash betiğinde sinyaller trap deyimi ile yakalanılar. <b>trap</b> <b>komut adı</b> <b>sinyal numarası</b> şeklinde trap deyimini kullanabiliriz. Biz betiğimizde echo komutunu kullanarak gelen sinyal numarası karşılık yakalanan sinyalin alındığını belirten bir mesaj yazdıracağız.Bununla birlikte bir for döngüsü kullanarak birer saniye aralıklarla “sinyal bekleniyor...” yazısını yazarak sinyal in gelmesini beklemeye başlıyacağız.

```
#!/bin/bash
trap ' echo "SIGTERM sinyali yakalandi!" ' 2

trap ' echo "SIGINT sinyali yakalandi!" ' 15

for (( c=1; c<200; c++ ))
  do
    echo "Sinyal bekleniyor..."
    sleep 1
  done
```

Betiğimizi sinyal.sh olarak kaydedelim.Çalıştırma izni vermek ve çalıştırmak için sırasıyla terminale

```
chmod +x sinyal.sh
./sinyal.sh
```

yazalım.

Çalışan betiğimizin PID değerini kullanarak sinyal gönderebiliriz.Bu değeri bulmak için terminale

```
ps -e | grep sinyal
```

yazalım.

<a href="/assets/images/ps-e.png" imageanchor="1">
	<img style="display: block;margin: 0 auto;" src="/assets/images/ps-e.png"/>
</a>

Betiğimizin PID değerini öğrendiğimize göre sinyal göndermeye başlayabiliriz.
TERM sinyalini,

```
kill -2 11542
```

```
kill 11542
```

```
kill -TERM 11542
```

bu üç komutdan birini kullanarak ya da betik penceremizin üzerine gelerek <b>ctrl+c</b> tuşlarını kullanarak da TERM sinyalini gönderelim.

INT sinyalini

```
kill -15 11542
```

```
kill -INT 11542
```

bu iki komutdan birini kullanarak gönderelim.

Son olarak ise KILL sinyalini

```
kill -9 11542
```

```
kill -KILL 11542
```

bu iki komutdan birini kullanarak gönderelim.

<a href="/assets/images/betik.png" imageanchor="1">
	<img style="display: block;margin: 0 auto;" src="/assets/images/betik.png"/>
</a>

Yazımızın başında söyledeğimiz üzere KILL sinyalinin bir prosese gönderilmesi durumda bu proses her zaman son bulacağını söylemiştik.Resimde görüldüğü üzere prosesimizin çalışması KILL sinyalinden dolayı killed yazarak son bulmuş oldu. Yazımızın sonuna geldik.Anlamadığınız yerleri yorum olarak yazarsanız,yardımcı olabilirim.İyi Çalışmalar.

## Referans
* http://man7.org/linux/man-pages/man7/signal.7.html