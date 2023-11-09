# Kamera Yönetim Sistemi

## Nasıl Çalıştırılır

1.[Exiftool](https://exiftool.org/) sayfasından exiftool indirilir ve işletim sistemine göre kurulur.

(Projede MacOS kullanıldı.)

2.Virtual environment kurulur

```bash
# virtual environment oluşturulur
python -m venv .venv

# venv aktifleştirilir
. .venv/bin/activate (macOS)
```

3.Paketler indirilir

```bash
pip install -r requirements.txt
```

3.model.py ile etiketleme yapmak için

```bash
# model.py dosyası iki input ister,
# -etiketleme yapılacak resimlerin dosya yolu
# -çıktıların yolu, camera1 veya camera2
python src/model.py
```

4.app.py dosyası çalıştırılır

```bash
python UI/app.py
```

Şimdilik iki adet kullanıcı var

- kullanıcı adı: test_user_3
- şifre: 123456
  (camera1 atanmış)

- kullanıcı adı: test_user_4
- şifre: 123456
  (camera2 atanmış)

Yeni oluşturulan kullanıcılara yeni kamera atamak için kamera dosya yolu oluşturulmalı.

```bash
mkdir ./UI/static/images/<camera{id}>
```

Ardından register sayfasından oluşturulan yeni kullanıcı yeni kameraya atanmalıdır

UI dosya yolunda python shell açılır

```
# örnektir
>>> from app import app, User, Camera, db
>>> cam2 = Camera.query.filter_by(name='Camera 2').first()
>>> cam2.owner = User.query.filter_by(username='test_user_4).first().id
>>> db.session.add(cam2)
>>> db.session.commit()

# kamera atanması doğrulama
>>> c2 = Camera.query.filter_by(name='Camera 2').first()
>>> c2.user
<User 4>
```
