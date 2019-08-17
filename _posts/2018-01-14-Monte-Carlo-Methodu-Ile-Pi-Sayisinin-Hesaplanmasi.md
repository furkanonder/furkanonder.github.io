---
title: Monte Carlo Metodu ile Pi Sayısının Hesaplanması
comments: true
layout: post
date: '2018-01-14'
author: Furkan Önder
categories:
- Python
- Java
- C
tags:
- Monte Carlo Metodu İle Pi Sayısı
description: Monte Carlo Metodu ile Pi Sayısının Hesaplanması
---

Merhaba,
Bugünki yazımda Monte Carlo Metodu ile pi sayısının hesaplanmasını anlatacağım.Öncelikle  Monte Carlo Metodu’nu tanıyalım.

Monte Carlo Metodu, genel olarak istatistiksel simülasyonların yapılması için rastgele  sayılardan  faydalanılan bir metot olarak tanımlayabiliriz. Los Alamos Bilimsel Laboratuar’ından John Von Neumann, Stan Ulam ve Nick Metropolis adlarında üç bilim adamı tarafından ortaya çıkarılmıştır.Monte Carlo metodu ilk defa II.Dünya Savaşı sırasında atom bombasının geliştirilmesi ile ilgili problemlere uygulanmıştır.Günümüzde bu metot,Hücre Simülasyonu, Borsa Modelleri, Dağılım Fonksiyonları,Atom ve Molekül Fiziği, Nükleer Fizik modellerini test eden simülasyonlarının hesaplanmalarında kullanılır.

Şimdi Monte Carlo Metodu ile pi sayısının hesaplanmasına geçelim.Alanı 4 birim kare olan bir kare düşünelim. Karenin içine de teğet olarak yerleştirilmiş  yarıçapı 1 birim olan bir çember(birim çember) çizelim.

<a href="/assets/images/cember.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;height:300px;width:300px;" src="/assets/images/cember.png"/>
</a>

Karenin içine kordinatları Z(a, b) noktası gibi rastgele atışlar gerçekleştirelim.Yaptığımız rastgele atışların bir kısmı çemberin içinde bir kısmı ise dışında olacaktır.Yapılan atışların:

<a href="/assets/images/ydenk.png" imageanchor="1">
  <img src="/assets/images/ydenk.png" style="display: block;margin: 0 auto;height:260;width:260;"/>
</a>  

olarak hesaplanır.Elde ettiğimiz bu ifadeyi 4 ile çarptığımızda ise yaklaşık olarak pi sayısını elde ederiz.

<a href="/assets/images/atis.gif" imageanchor="1">
  <img src="/assets/images/atis.gif" style="display: block;margin: 0 auto;height:300px;width:300px;"/>
</a>  

<span style="text-align: center;">Yapılan rastgele atışların simule edilmiş hali</span>

Programlama dilleri ile Monte Carlo Metodu'nu kullanılarak pi sayısının hesaplanması için yazılmış olan kodları inceleyelim.

Python:

```
import random
icerde = 0

for atis_sayisi in range(0, 1000000):
    a = random.random()
    b = random.random()
    z = (a*a+b*b)**0.5
    if z < 1:
        icerde += 1
atis_sayisi += 1

print("Pi sayisinin yaklasik degeri:", 4.0 * icerde / atis_sayisi)
```

C:

```
#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
int main(){
  double a,b;
  float atis_sayisi=0,icerdeki=0,pi,z;
  srand(time(NULL));

  for (int i = 0; i < 1000000;i++){
    atis_sayisi++;
    a = (double)rand()/RAND_MAX*2.0-1.0;
    b = (double)rand()/RAND_MAX*2.0-1.0;
    z = sqrt(pow(a,2)+pow(b,2));
    if(z<1)
    icerdeki+=1;
  }

  pi = 4*(icerdeki/atis_sayisi)*1.0;
  printf("Pi sayisinin yaklasik degeri:%f\n",pi );

  return 0;
}
```

Java:

```
import java.util.Random;

public class MonteCarlo {
  private static Random rgen = new Random();

  public static void main(String[] args) {

    int atis_sayisi = 0;
    int icerde = 0;

    for(int i = 0; i<1000000; i++){
      double a = 2 * rgen.nextDouble() - 1;
      double b = 2 * rgen.nextDouble() - 1;
      atis_sayisi +=1 ;
      if (Math.pow(a, 2) + Math.pow(b, 2) < 1) {
        icerde += 1;
      }
    }
    double pi = 4*(icerde*1.0/atis_sayisi);
    System.out.println("Pi sayisinin yaklasik degeri: " + pi);
  }
}
```

Kodlarda anlamadığınız yerleri yorum olarak yazarsanız, yardımcı olabilirim. İyi Çalışmalar.

## Referans
* https://en.wikipedia.org/wiki/Monte_Carlo_method