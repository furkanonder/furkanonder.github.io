import sqlite3
import time
import datetime
import urllib.request
import json

try:
    vt = sqlite3.connect('kur.db')
    if (vt):
        imlec = vt.cursor()
        try:
            imlec.execute('''
            CREATE TABLE kurTablosu(
            sira INTEGER PRIMARY KEY AUTOINCREMENT,
            alis REAL,
            satis REAL,
            zaman VARCHAR )''')
            print("Tablo oluşturuldu.")
            vt.commit()
            vt.close()
        except:
            print("Tablo oluşturulamadı veya tablo mevcut.")
    else:
        print("Veri tabanı bağlantısı kurulamadı.")
except:
    print("Veri tabanı oluşturulamadı.")


def vtEkle(alis, satis, tarihVeSaat):
    vt = sqlite3.connect('kur.db')
    imlec = vt.cursor()

    sorgu = 'INSERT INTO kurTablosu (alis,satis,zaman) VALUES ('
    sorgu += '"' + alis + '",'
    sorgu += '"' + satis + '",'
    sorgu += '"' + tarihVeSaat + '")'

    try:
        imlec.execute(sorgu)
        vt.commit()
        vt.close()
    except:
        print("Veriler eklenemedi.")

    vt.close()


def dolar():
    url = 'https://www.doviz.com/api/v1/currencies/USD/latest'
    istek = urllib.request.Request(url)
    i = urllib.request.urlopen(istek).read()
    veri = json.loads(i.decode('utf-8'))

    return veri['buying'], veri['selling']

# vtEkle(str(alis), str(satis), str(datetime.datetime.now())) bu veri tipleri düzenlenmeli


while True:
    try:
        alis, satis = dolar()
        print("Dolar:\n", "Alış:", alis, "Satış:", satis, "Tarih ve Saat:", datetime.datetime.now())
    except:
        print("Veriler okunamadı.")
        break

    try:
        vtEkle(str(alis), str(satis), str(datetime.datetime.now()))
        print("Veriler veritabanına eklendi.")
    except:
        print("Veriler veritabanına eklenemedi.")

    time.sleep(300)
