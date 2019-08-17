---
title: Python ve C ile Faktöriyel
comments: true
layout: post
date: '2016-02-25'
author: furkan önder
categories:
- python
tags:
- faktöriyel hesaplama
description: Python ve C ile Faktöriyel hesaplama
---

Merhaba, 
bu yazıda sizlere python ve c ile faktöriyel almayı göstereceğim.
Öncelikle faktöriyelin ne olduğunu kısaca açıklayalım:
Faktöriyel, pozitif bir tamsayının kendisinden önceki bütün tamsayılarla 1'e inilinceye kadar çarpılması sonucunda elde edilen çarpımdır. n sayısının faktöriyeli, n! şeklinde gösterilir.

Örneğin;
5 sayısının faktöriyeli 5.4.3.2.1= 120 olarak hesaplanır. Faktöriyel hakkında daha fazla bilgi almak için <a href="https://en.wikipedia.org/wiki/Factorial" target="_blank"> burayı </a>ziyaret edebilirsiniz.Şimdi faktöriyel için python ve c ile yazılmış olan kodları inceleyelim;

C:

```
#include<stdio.h> 
int main(){  
    int sayi, sonuc=1; 
  
    printf("Faktoriyelini almak istediginiz sayiyi  giriniz: ");
    scanf("%d", &sayi); 
		
    // for ile bir döngü oluşturduk.Döngünün içinde i değişkeni oluşturup, 1'e eşitliyoruz.
    //i değiskeni, sayi değişkenine eşit ya da büyük olmasına kadar döngü  tekrar edecek.
    //i değişkeni döngünün her tekrarında  arttırılacak.
		
    for(int i=1;i<=sayi;i++){ 
    sonuc = sonuc*i; 
    }
    printf("%d sayisinin faktoriyeli %d sayisina esittir.",sayi, sonuc);  
  
  getchar();
  return 0; 
}
```
Python:

```
sayı = int(input('Faktöriyelini almak istediğiniz sayıyı giriniz : '))
faktöriyel = 1

#For yapısı ile bir döngü oluşturuyoruz.
#range(sayı) ile girdiğimiz sayı kadar döngünün tekrar etmesini sağlıyoruz.
for i in range(sayı):    
    faktöriyel = faktöriyel *(1+i)

print(sayı,"sayısının faktöriyeli",faktöriyel,"sayısına eşittir.")
```

Kodlarda anlamadığınız yerleri yorum olarak yazarsanız, yardımcı olabilirim.İyi Çalışmalar.

## Referans
* https://en.wikipedia.org/wiki/Factorial