import sqlite3
import time
import datetime
import urllib.request
import json


vt = sqlite3.connect('kur.db')
imlec = vt.cursor()

try:
    imlec.execute('''
    CREATE TABLE kurTablosu(
    sira INTEGER PRIMARY KEY AUTOINCREMENT,
    alis VARCHAR,
    satis VARCHAR,
    zaman VARCHAR )''')
    vt.commit()
    vt.close()
except:
    print("Tablo oluşturulamadı veya tablo mevcut.")


def vtEkle(alis, satis, TarihVeSaat):
    vt = sqlite3.connect('kur.db')
    imlec = vt.cursor()
    imlec.execute("INSERT INTO kurTablosu (alis,satis,zaman) VALUES(?,?,?)", (alis, satis, TarihVeSaat))
    vt.commit()
    vt.close()


def dolar():
    url = 'https://www.doviz.com/api/v1/currencies/USD/latest'
    istek = urllib.request.Request(url)
    i = urllib.request.urlopen(istek).read()
    veri = json.loads(i.decode('utf-8'))

    return veri['buying'], veri['selling']


while True:
    alis, satis = dolar()
    print("Alış:", alis, "Satış:", satis, "Tarih ve Saat:", datetime.datetime.now())
    vtEkle(str(alis), str(satis), str(datetime.datetime.now()))
    time.sleep(300)
