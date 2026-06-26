# ilanSearch 🚀

**Türkiye'deki Senior Front-End Developer İlanlarını Otomatik Bulan Script**

## 📋 Özellikler

- 🏢 **30+ Türk Yazılım Firması** kariyer sayfası taranır
- 🌐 **Kariyer.net** ve **LinkedIn** entegrasyonu  
- 🎯 Akıllı **anahtar kelime filtresi** (Türkçe + İngilizce)
- 📊 **Güzel HTML Dashboard** - arama ve filtreleme
- 🔔 **Yeni ilan bildirimleri** (macOS)
- ⏰ **Otomatik tarama** - her X saatte bir

## 🚀 Kurulum & Kullanım

### 1. Tek Seferlik Kurulum ve Çalıştırma

```bash
cd ilanSearch
chmod +x run.sh
./run.sh
```

### 2. Manuel Kurulum

```bash
# Virtual environment oluştur
python3 -m venv .venv
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Scraper'ı çalıştır
python scraper.py
```

### 3. Otomatik Takip (Her 4 saatte bir)

```bash
# 4 saatte bir otomatik tara + macOS bildirimi
python watch.py

# Özel aralık (2 saat)
python watch.py --interval 2

# Sadece bir kez çalıştır
python watch.py --once
```

### 4. HTML Dashboard'u Aç

```bash
open output/report.html
```

## 📁 Dosya Yapısı

```
ilanSearch/
├── scraper.py          # Ana scraper
├── watch.py            # Otomatik takip botu  
├── dashboard.py        # Web sunucusu
├── companies.json      # Firma veritabanı
├── requirements.txt    # Bağımlılıklar
├── run.sh              # Tek tıkla başlat
└── output/
    ├── report.html     # HTML rapor (tarayıcıda aç)
    ├── latest.json     # Son tarama sonuçları
    └── known_ids.json  # Daha önce görülen ilanlar
```

## 🏢 Taranan Firmalar

| Firma | Platform |
|-------|----------|
| Trendyol | Teamtailor |
| Hepsiburada | Teamtailor |
| Getir | Lever |
| Dream Games | Lever |
| Insider | Özel |
| Garanti BBVA Technology | Teamtailor |
| Yapi Kredi Technology | Teamtailor |
| Turkcell | Teamtailor |
| BtcTurk | Teamtailor |
| Paribu | Teamtailor |
| Sahibinden | Teamtailor |
| ... ve 20+ firma daha | |

## 🎯 İlan Filtreleme Kriterleri

Script şu pozisyonları arar:
- `Senior Front-End Developer`
- `Senior Frontend Developer`  
- `Senior React Developer`
- `Senior Vue.js Developer`
- `Lead Front-End Developer`
- `Kıdemli Front-End Developer`
- `Senior UI Engineer`
- ve daha fazlası...

## ➕ Yeni Firma Eklemek

`companies.json` dosyasına ekleyin:

```json
{
  "name": "Firma Adı",
  "url": "https://firma.com",
  "career_url": "https://firma.teamtailor.com/jobs",
  "type": "teamtailor",
  "logo": "🏢"
}
```

**type** seçenekleri: `teamtailor`, `lever`, `custom`

## 📝 Notlar

- Bazı siteler JS render gerektiriyor → Playwright desteği eklenebilir
- LinkedIn tam tarama için oturum açmak gerekebilir
- İstekler arası 1.2sn bekleme → site ban'dan kaçınır
- Tüm sonuçlar `output/latest.json`'a kaydedilir

---
*Başarılar! 🍀*
