---
title: C kodunu gdb ile disassemble etmek
comments: true
layout: post
date: '2019-08-23 14:00:00'
author: furkan önder
categories:
- C
- gdb
- gcc
- tersine mühendislik
tags:
- gdb kullanımı
- Tersine Mühendislik
description: Gdb hata ayıklayıcısı ile C kodunun disassemble edilmesi
---

C kodu yazmak eğlencelidir özellikle gcc ile derliyorsunuz :D [Gcc](https://gcc.gnu.org/) derleyicisini biliyorsanız, hata ayıklayıcısı olan [gdb](https://www.gnu.org/software/gdb/)'yi bilirsiniz.Mükemmel bir debugger... Gdb'yi ilk kullandığım zamanlarda çok karmaşık geliyordu.Anlamak için çaba sarf ettim.Öğrendiklerimide yazmaya karar verdim.

## Neler lazım?
* x86_64 bir Gnu/Linux dağıtımı
* Gcc ve gdb
* Assembly programlama bilgisi

Assembly için [adresinde](https://0xax.github.io/asm_1/) bulunan yazı dizisini takip edebilirsiniz ya da bu yazı dizisinin [çevirisini](https://github.com/furkanonder/asm) takip edebilirsiniz.Bunların dışında assembly için yazılmış birçok kitap bulunuyor onlara da bakabilirsiniz....

## Başlıyoruz
Disassemble etmesi kolay olması için basit bir kod parçasından başlayalım.
Kodumuz sadece 0 değerini döndürüyor.

```
int main(){
    return 0;
}
```

Gcc ile derleyelim.

```
gcc test.c -o test
```

Derlenmiş olan dosyamızı gdb ile açalım.

```
gdb test
```

Gdb de varsayılan olarak AT&T sözdizimine sahip assembly komutları geliyor.Ben bunu intel söz dizimine çeviriyorum.
Okuması daha kolay geliyor...

```
set disassembly-flavor intel
```

Söz dizimini ayarladıktan sonra main fonksiyonuzumu dissamble edelim.

```
disassemble  main
```

Karşımıza böyle bir şey çıktı...

```
Dump of assembler code for function main:
   0x0000000000001119 <+0>:	    push   rbp
   0x000000000000111a <+1>:	    mov    rbp,rsp
   0x000000000000111d <+4>:	    mov    eax,0x0
   0x0000000000001122 <+9>:	    pop    rbp
   0x0000000000001123 <+10>:	    ret    
End of assembler dump.
```

İlk satıra baktığımızda 0x0000000000001119 adresini ve yanında ise "push rbp" şeklinde bir assembly komutu görüyoruz.

## Peki bunlar ne anlama geliyor?
Her fonksiyon bir prologue(başlangıç) ve bir epilogue(kapanışın) işleminin içine yerleştirilmiştir.<+0> ile <+1>'deki komutlar prologue işlemidir.Prologue işlemi fonksiyonunun kullanacağı register ve stack'i hazırlamak için yapılır.Rbp, geçerli stack çerçevesinin tabanını işaret eden bir register'dır.Burada rbp, main fonksiyonun stack çerçevesinin tabanına işaret ediyor.Rsp ise stack işaretçisi registeri'dır, geçerli stack çerçevesinin üstünü işaret eder.

"push rbp" komutu ile rbp' stack'in tabanına yerleştiriliyor."mov rbp,rsp" komutu rsp'nin değerini rbp'ye kopyalanıyor.İkisinin de adresi stack çervesinin tabanını gösteriyor.Stack kullanıma hazır böylece prologue işlemimiz bitti.Stack'e bir şey koyulduğunda rsp stack'in üstünü işaret ederek azalacak.Peki neden azalıyor? Çünkü stack, yüksek hafıza adresinden düşük adrese doğru büyür.

"mov eax, 0x0" ise C kodundaki "return 0"'a karşılık geliyor.Eğer "return 0" yerine "return 1" yazsaydık, "mov eax 0x1" şeklinde bir komut görürdük.<+9> ve <+10>'daki komutlar ise epilogue(kapanış) işlemidir.Prologue işlemlerinin tersi yapar."pop rbp" komutu ile stack'e pushlanan rbp'yi çıkarır."ret" komutu ile fonksiyonun dönüş değerini döndürür.

Referanslar:
* http://en.wikipedia.org/wiki/Call_stack
* https://en.wikipedia.org/wiki/Function_prologue
* https://en.wikibooks.org/wiki/X86_Disassembly/The_Stack