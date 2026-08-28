# Yapay Zeka ile Müşteri Yorum Analizi

Türkçe e-ticaret yorumlarını Google Gemini ile duygu analizine sokan, sonuçları
PostgreSQL'de saklayan ve REST API üzerinden sunan bir backend projesi.

Yorum girer, **pozitif / negatif / nötr** etiketi, bir güven skoru ve modelin
gerekçesi çıkar.

---

## Durum

| Adım | Durum |
|---|---|
| Gemini API entegrasyonu | ✅ Tamamlandı |
| PostgreSQL kalıcı kayıt | ✅ Tamamlandı |
| FastAPI REST katmanı (4 uç nokta) | ✅ Tamamlandı |
| Gerçek veri + toplu analiz + doğruluk ölçümü | 🚧 Devam ediyor |
| Streamlit arayüz | ⏳ Planlandı |
| Docker + deploy | ⏳ Planlandı |

Sistem şu an uçtan uca çalışıyor: `tarayıcı → FastAPI → Gemini → PostgreSQL`.

---

## Mimari

```
İstemci
 │  POST /analysis  {"comment": "..."}
 ▼
FastAPI (app/main.py)        → istek doğrulama (Pydantic)
 ▼
analysis_service.py          → iş akışı: analiz et + kaydet
 ├──► gemini_service.py      → prompt kur, Gemini'yi çağır, JSON'a çevir
 └──► database.py            → psycopg2 ile INSERT
 ▼
PostgreSQL (analyses tablosu)
```

| Katman | Teknoloji |
|---|---|
| Dil | Python 3.12 |
| API | FastAPI + Uvicorn |
| Yapay zeka | Google Gemini (`google-genai`) |
| Veritabanı | PostgreSQL 18, **raw SQL** (psycopg2) |
| Doğrulama | Pydantic |

---
        
## Kurulum

**Gereksinimler:** Python 3.12+, PostgreSQL, bir Gemini API anahtarı
([Google AI Studio](https://aistudio.google.com/apikey)'dan ücretsiz alınır).

```bash
git clone <repo-adresi>
cd ai_musteri_yorum_analizi

python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

Veritabanını oluştur:

```bash
createdb yorum_analizi
psql yorum_analizi -f sql/schema.sql
```


Ortam değişkenlerini ayarla:

```bash
cp backend/.env.example backend/.env
```

Ardından `backend/.env` dosyasını bir editörde açıp iki değeri doldur:

| Değişken | Ne yazılacak |
|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey)'dan alınan anahtar |
| `DATABASE_URL` | Örnekteki `postgresql:///yorum_analizi` yerel kurulumda (peer auth) çalışır. Postgres'in şifre istiyorsa: `postgresql://kullanici:sifre@localhost:5432/yorum_analizi` |

Çalıştır:

```bash
cd backend
uvicorn app.main:app --reload
```

İnteraktif dokümantasyon: **http://127.0.0.1:8000/docs**

---
## API

| Yöntem | Uç nokta | Açıklama |
|---|---|---|
| `GET` | `/` | Servisin ayakta olduğunu bildirir |
| `POST` | `/analysis` | Yorumu analiz eder, kaydeder, sonucu döner |
| `GET` | `/analysis/history?limit=10` | Son analizler (yeniden eskiye) |
| `GET` | `/analysis/stats` | Duygu dağılımı ve toplam sayı |

**Örnek istek**

```bash
curl -X POST http://127.0.0.1:8000/analysis \
  -H "Content-Type: application/json" \
  -d '{"comment": "kargo çok geç geldi berbat"}'
```

**Örnek cevap**

```json
{
  "sentiment": "negatif",
  "confidence": 0.98,
  "explanation": "Yorumda kargo gecikmesinden şikayet ediliyor ve 'berbat' ifadesi kullanılıyor.",
  "id": 5
}
```



