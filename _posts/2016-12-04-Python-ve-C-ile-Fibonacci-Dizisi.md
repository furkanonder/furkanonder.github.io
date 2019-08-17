---
title: Python ve C ile Fibonacci Dizisi
comments: true
layout: post
date: '2016-12-04'
author: furkan önder
categories:
- python
- C
tags:
- fibonacci dizisi
description: Python ve C ile Fibonacci Dizisi hesaplama
---

Merhaba, 
bugün ki yazımda sizlere python ve c ile fibonacci dizisi oluşturmayı göstereceğim.Kısaca fibonacci dizisini tanıyalım:
Fibonacci dizisi her sayının kendinden önceki sayı ile toplanması sonucu oluşan bir sayı dizisidir.

<a href="/assets/images/fib.jpg" imageanchor="1">
  <img style="display: block;margin: 0 auto;" src="/assets/images/fib.jpg" />
</a>

n yerine sırasıyla 0,1,2,3,4,5,6,7... şeklinde değerler verdiğimizde 0,1,1,2,3,5,8,13…şeklinde bir fibonacci dizisi elde ederiz.Fibonacci dizisi ile ilgili daha ayrıntılı bilgi almak için <a href=" https://tr.0wikipedia.org/wiki/Fibonacci_dizisi" target="_blank"> burayı </a>ziyaret edebilirsiniz.

Şimdi fibonacci dizisi için python ve c ile yazmış olduğum kodları inceleyelim;

C:

```
#include<stdio.h> 
int main(){
   int n=10, a = 0, b = 1, deger;
     
   //Bir döngü oluşturuyoruz.Bu döngü b değeri n den büyük olana kadar tekrar edecek.
   for( ; b < n; ){
     deger = a+b;
     a = b;
     b = deger;
     printf("%d\n",b);
    }
    
  getchar();
  return 0;  
}
```

```
n=10
a=1
b=0

#Bir döngü oluşturuyoruz.Bu döngü, b değeri 10'dan büyük olana kadar tekrar edecek.
while b < n:
    deger= a+b
    a = b
    b = deger
	  print(b)

```
Bu kodların konsol çıktısı "1 1 2 3 5 8 13" şeklinde olur.
Kodlarda anlamadığınız yerleri yorum olarak yazarsanız, yardımcı olabilirim.İyi Çalışmalar.

## Referans
* https://en.wikipedia.org/wiki/Fibonacci_number