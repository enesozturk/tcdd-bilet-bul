# TCDD Bilet Kontrolü

Bu proje TCDD'nin seferlerini devamlı olarak sorgulayıp, bulunduğu anda telefonunuza bildirim göndermek için yazılmıştır. 

    Doğu Ekspresi için bilet almak istediğimde farkettim ki seferler farklı saatlerde açılıyor. Açıldığı zaman da hemen doluyor. Bu konuda yardımcı olması amacı ile yazılmış bir uygulama. 

Sefer sorgulama için kullanılan API hakkında bilgiyi [buradan](https://github.com/aliahmet/tcdd) mutlaka okuyunuz.


## Kullanımı

- Proje içinde [virtualenv](https://virtualenv.pypa.io/en/latest/) oluşturun.
  - `virtualenv -p python3 env`
- Virtual Environment'i aktifleştirin
  - `source env/bin/activate`
- Gerekli paketleri indirin
  - `pip install -r requirements/dev.txt`
- Kod kısmında gerekli kısımları değiştirip projeyi başlatın
  - `python tcdd.py`

Örnek sorgu:
```python
...
tarih = date(2019, 1, 1)
...
cevap = tcdd.seferSorgula(
    binisIstasyonu='Ankara Gar', 
    inisIstasyonu='Kars', 
    gidisTarih=tarih
    )
...
```

Telefonunuza bildirim gönderilmesini istiyorsanız. Şu adımları takip edin. 

- https://www.pushsafer.com sitesine üye olun
- Mobil uygulaması olan PushSafer'i telefonunuza indirip giriş yapın (Android/IOS)
- Web site üzerinden `private key` ve `device key` bilgilerini kopyalayıp projede `PushSafer` class'ı içinde gerekli yerlere yapıştırın

Mobil bildirim devre dışı bırakmak isterseniz *sendNotification* metodunu yorum satırı yapın

```python
if "başarılı" in cevapMesaj:
    # send notification to yourself
    # pushSafer.sendNotification('Doğu Ekpresi', 'Doğu Ekpresi bileti seni bekliy--> ' + mesajIcinTarih)
    isSend = True
    logging.info(mesajIcinTarih + 'için sefer bulundu')
    print("Sefer BULUNDU!")
    break
```
