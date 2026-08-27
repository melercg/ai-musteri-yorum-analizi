"""
Uygulamanin ayarlarini tek merkezden okur.

Adimlar:
    1. .env dosyasinin tam yolunu bul
    2. load_dotenv ile yukle
    3. GEMINI_API_KEY ve DATABASE_URL'i oku
    4. Eksik varsa hata ver

.env dosyasinda olmasi gerekenler:
    GEMINI_API_KEY=...
    DATABASE_URL=postgresql:///yorum_analizi
"""
# uygulamanın ayarlarını tek merkeszden okumak için :
import os
from pathlib import Path
from dotenv import load_dotenv

# backend/.env dosyasinin tam yolu
# __file__ = backend/app/core/config.py
# parents[0] = core   parents[1] = app   parents[2] = backend
# .env dosyası backend/ içinde olduğu için indis 2.
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Erken hata (fail fast): eksik ayar varsa uygulama daha ilk import'ta dursun,
# ilk Gemini çağrısında değil. Hatanın sebebi böyle net görünür
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY bulunamadi. .env dosyasina ekleyin.")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL bulunamadi. .env dosyasina ekleyin.")
