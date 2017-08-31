TCDD Gayri Resmi API

Bu kodun Türkiye Cumhuriyeti Devlet Demiryolları ile hiç bir ilişkisi yoktur. Tamamen gayri resmi ve bağımsız bir API'dir. 

Kullanımı izne tabi olabilir. 

Kullanımından doğacak her sonuç kullanan kişiye ait.

Örnek Sefer Sorgulama:
```python
from tcdd import TCDDClient
import datetime

tcdd = TCDDClient()
yarin = datetime.date.today() + datetime.timedelta(days=1)
cevap = tcdd.seferSorgula(
    binisIstasyonu='İstanbul (Pendik)', 
    inisIstasyonu='Ankara Gar', 
    gidisTarih=yarin
    )

if cevap.is_successful():
    data = cevap.data()
    ...
```