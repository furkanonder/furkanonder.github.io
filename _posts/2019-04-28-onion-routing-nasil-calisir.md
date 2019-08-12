---
title: Onion Routing Nasıl Çalışır?
comments: true
layout: post
date: '2019-04-28 00:30:00'
author: furkan önder
categories:
- tor
- oninon routing
tags:
- oninon routing nedir
- oninon routing nasıl çalışır
description: Tor ağındaki onion routing yapısının çalışma şekli
---

Tor projesi ilk olarak ABD Deniz Kuvvetleri tarafından askeri bir gizli ağ projesi olarak haberleşmesini korumak için geliştirildi. Ancak 2004 yılına gelindiğinde ABD Deniz Harp Araştırma Laboratuvarı Tor’u açık kaynak lisanslı bir proje haline getirip herkese açtı.<br>

Günümüzde, bir çok amaç için tor kullanabiliyor.Örneğin, normal bir internet kullanıcıları arama motorları tarafından bilgilerinin toplanmalarını ve satılmalarından pek hoşlanmayabilirler.Arama motorlarında arattığınız bir içeriği sonraki sayfalarda reklam olarak hiç gördünüz mü?İşte bu bir sadece gözle görülür bir örnek.Tor,insan hakları aktivistleri ve gazeteciler tarafından kullanılır.Örneğin, bir bölgede yaşanan istismarları ve bildirmek için kullanılabilir. Bu bölgeler yasalar dahilinde olsalar bile, güvenli oldukları anlamına gelmez. Tor, sesinizi yükseltirken size koruma sağlar.Bunların yanında sağladığı gizlilik nedeniyle Tor ağının uyuşturucu, ilaç ve silah kaçakçılığı, pornografi ve kara para aklama faaliyetleri için de kullanıldığı tespit edilmiştir.<br>

Tor hakkında kısa bir fikir edindiğimize göre asıl konumuza geçebiliriz.Bir web sitesiyle tor ağı aracıyla iletişim kurmaya çalışağız.Şemaya incelediğimiz ilgisayarımızı,düğüm(node)’lerı ve hedef sitemizi görüyorüz.Peki, düğüm(node) nedir? Düğüm, Tor ağında trafik alan ve ileten gönüllü sunuculardır.Sizde bir tor düğümü kurarak tor ağına destek verebilirsiniz.Tor ağını kullanarak bir  web sitesine ulaşmaya çalıştığınızda isteğiniz düğüm denilen yapılan üzerinden aktarılır.

<a href="/assets/images/onion/tor-0.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 33em;"  src="/assets/images/onion/tor-0.png"/></a><br/>

Web sitesine bir mesaj gönderelim. Şekilde 3 tane node(düğüm) bulunuyor.Mesajmızı, her düğüm boyunca simetrik bir anahtar şifreleme sistemi olan AES kullanarak şifreliyoruz. Bu şifrelemeyi çözmek için ise Diffie-Hellman anahtar değişimi yöntemi kullanılacağız.<br>

Kulağa biraz karışık geldi mi? Basit bir örnekleme yapalım.Şifreleme yapısını kutu olarak düşenelim.Yani, göndereceğimiz mesajı bir kutu içinde sakladığımızı düşenelim.

<a href="/assets/images/onion/tor-1.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 33em;"  src="/assets/images/onion/tor-1.png"/></a><br/>
Mesajımız siyah bir kutunun içine koyduğumuzu düşünelim.Bu siyah kutuyuda ise kırmızı bir kutuya son olarak bu kırmızı kutuyuda mavi bir kutuya koyalım.Üç kutumuz var; bu 3 node boyunca 3 kere mesajımızı şifrelediğimiz anlamına geliyor.
<a href="/assets/images/onion/tor-2.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 33em;"  src="/assets/images/onion/tor-2.png"/></a><br/>
Göndereceğimiz mesajımız iç içe 3 kutudan oluşuyor.
Kutumuzu yolumuzdaki ilk düğüm olan düğüm 1’e gönderiyoruz Mavi kutuyu alan düğüm , Diffie-Hellman  yöntemi ile kutuyu açar.Ama yine gördüğü şey bir kırmızı renkte bir kutu olur.Bu durumda düğüm, kutu içindeki mesajdan haberder değildir.
<a href="/assets/images/onion/tor-3.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 33em;"  src="/assets/images/onion/tor-3.png"/></a><br/>

Daha sonra düğüm 1, kutuyu  düğüm 2’ye gönderirir. Düğüm 2, gelen kırmızı kutuyu açar. Bu durumda gördüğü siyah bir kutu olur.Kutu içindeki mesajdan haberder değildir ve kutuyu asıl olarak kimin gönderdiğinden haberi yoktur.Yani tek bildiği, düğüm 1'in ona bir  kırmızı bir kutu gönderdiği ve elindeki siyah kutuyu Düğüm 3'e göndermesidir.
<a href="/assets/images/onion/tor-4.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 33em;"  src="/assets/images/onion/tor-4.png"/></a><br/>

Daha sonra düğüm 2, kutuyu  düğüm 3 ‘e gönderirir.Artık son düğümdeyiz.
<a href="/assets/images/onion/tor-5.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 33em;"  src="/assets/images/onion/tor-5.png"/></a><br/>

Düğüm 3,  düğüm 2’nin ona verdiği siyah kutuyu açar. Böylece mesajın ne olduğunu ve nereye gittiğini bilir ancak kimin gönderdiğini bilmez. Tek bildiği şey, Düğüm 2'ün ona bir kutu yolladığı ve bu kutunun içindeki mesajı web sitesine göndermesidir.Ve tabiki yoldaki diğer düğümlerin varlığından haberi yok.Mesajımız tor ağı ile web sitesine ilettik.Anlatması kolay olsun diye şemaya 3 node ekledim, bu sayı daha fazla olabilir.<br>

<h1>Peki websitesi bize nasıl yanıt yolluyor?</h1>

Düğüm 3, mesajımıza bir şifreleme katmanını ekler. Web sitenesine kimin asıl istekde bulunduğu bilmez.Bildiği Düğüm 2'ün ona bir istek gönderdiği ve yanıt iletisini Düğüm 2'e göndermesidir.Düğüm 2’ye gelindiğinde ise bu düğümde bir şifreleme katmanını ekler ve düğüm 1’e gönderir.Son olarak düğüm 1’e geliriz.Şimdi, mesajımız tamamen şifrelenmiştir, hala mesajın ne içerdiğini bilen sadece  Düğüm 3tür. Mesajı kimin yaptığını bilen ise Düğüm 1'dir. Tüm simetrik anahtarları kullanarak şifreleme katmanlarını çözeriz ve websitesinin gönderdiği yanıtı elde ederiz.<br>

Biz örnekleme yaparkan kutu yapısını kullandık.Ama başlıktaki onion ne anlama geliyor?Eğer bir soğanı incelediğiyseniz üst üste bir çok zardan(kabuk) oluştuğunu görürsünüz.Bu üst üste bir çok kez şifreleme yapmamıza benziyor.Bundan dolayı bu iletim yöntemin ismi <b>onion routing</b>’dir.Biraz uzun bir yazı oldu.Umarım faydalı olmuştur.<br>

<b>Not:</b>Tor, internet trafiğini dünyanın çeşitli yerlerinde bulunan gönüllü sunucular aracılığıyla yaparak anonimlik kazanır ama gönderdiğimiz veri şifrelenip çözülmesinden dolayı internetin bağlantınızın  biraz yavaşlamasına sebep olur.