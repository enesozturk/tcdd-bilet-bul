import requests
import json
from datetime import date
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import time
import logging

class PushSafer():
    def sendNotification(self, baslik, mesaj):
        url = 'https://www.pushsafer.com/api' # Set destination URL here
        post_fields = {                       # Set POST fields here
            "t" : baslik,  #see push safer parameters on website https://www.pushsafer.com
            "m" : mesaj,
            "s" : 20,
            "pr": 2,
            "v" : 3,
            "i" : 9,
            "d" : deviceKey,
            "k" : "privateKey"
            }

        request = Request(url, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()

class TCDDResponse():
    def __init__(self, response):
        self.response  =response
        self.content = response.content

    def is_successful(self):
        return self.response.status_code < 300

    def data(self):
        return json.loads(self.content)

    def content(self):
        return self.content

class TCDDBaseClient():
    base_url = 'https://eybistrm.tcdd.gov.tr/WebServisWeb/rest/EybisRestApplication/'
    headers = {
        'Host': 'eybistrm.tcdd.gov.tr',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Authorization': 'mobilProd14:8Jh6g81dP4p72k',
        'Accept-Language': 'en-us',
    }
    cookies = {

    }
    def update_headers(self, new_headers):
        self.headers.update(new_headers)

    def update_cookies(self, new_cookies):
        self.cookies.update(new_cookies)

    def format_date(self, date):
        return date.strftime("%b %d, %Y %I:%M:%S %p")

    def _request(self, method, data):
        url = "%s%s"%(self.base_url, method)
        data.update({
            "dil": 0,
            'kanalKodu': '3',
        })
        return TCDDResponse(requests.post(url, headers=self.headers, cookies=self.cookies, json=data))

    def seferSorgulaRequest(self, data):
        _data = {
            'seferSorgulamaKriterWSDVO': data
            } 
        return self._request('seferSorgula', _data)

    def istasyonYukleRequest(self):
        return self._request('istasyonYukle', {})

    def nesneYukleRequest(self):
        return self._request('nesneYukle', {})

    def bolgeselBolgeOkuRequest(self):
        return self._request('bolgeselBolgeOku', {})

    def istasyonTrenSorgulaRequest(self, data):
        return self._request('istasyonTrenSorgula', data)

    def seferDetaySorgulaRequest(self, data):
        return self._request('seferDetaySorgula',data)

class TCDDClient(TCDDBaseClient):
    def seferSorgula(self, binisIstasyonu, inisIstasyonu,gidisTarih, aktarmalarGelsin=True, bolgeselGelsin=False, islemTipi=0, satisKanali=3, seyahatTuru=1, yolcuSayisi=1):
        data = {
            'aktarmalarGelsin': aktarmalarGelsin,
            'binisIstasyonu': binisIstasyonu,
            'bolgeselGelsin': bolgeselGelsin,
            'gidisTarih': self.format_date(gidisTarih),
            'inisIstasyonu': inisIstasyonu,
            'islemTipi': islemTipi,
            'satisKanali': satisKanali,
            'seyahatTuru': seyahatTuru,
            'yolcuSayisi': yolcuSayisi
            }
        return self.seferSorgulaRequest(data)
    
    def istasyonYukle(self):
        return self.istasyonYukleRequest()
        
    def nesneYukle(self):
        return self.nesneYukleRequest()

    def bolgeselBolgeOku(self):
        return self.bolgeselBolgeOkuRequest()

    def istasyonTrenSorgula(self, tarih, stationName):
        data = {
            "tarih": self.format_date(tarih),
            "stationName":stationName
        }
        return self.istasyonTrenSorgulaRequest(data)

    def seferDetaySorgula(self, seferId):
        data = {
            "seferId": seferId
        }
        return self.seferDetaySorgulaRequest(data)

tcdd = TCDDClient()
pushSafer = PushSafer()
isSend = False

logging.basicConfig(filename='logs.log', level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

tarih = date(2019, 1, 1)
mesajIcinTarih = tarih.strftime("%d/%m")

while(1):
    if isSend == False:
        cevap = tcdd.seferSorgula(
            binisIstasyonu='Kalkis İstasyonu',
            inisIstasyonu='Varis Istasyonu',
            gidisTarih=tarih
        )

        if cevap.is_successful():
            data = cevap.data()
            cevapMesaj = data['cevapBilgileri']['cevapMsj']
            if "başarılı" in cevapMesaj:
                    #send notification to yourself
                    pushSafer.sendNotification('Biletler Açıldı', 'Biletler seni bekliyor --> ' + mesajIcinTarih)
                    isSend = True
                    logging.info(mesajIcinTarih + 'için sefer bulundu')
                    print('Sefer BULUNDU')
                    break
            else:
                logging.info(mesajIcinTarih + ' için sefer bulunamadı')
                print('Sefer bulunamadı')

    time.sleep(5)