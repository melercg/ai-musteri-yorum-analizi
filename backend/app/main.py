"""
FastAPI uygulaması: HTTP uç noktaları.

Bu dosya iş mantığı içermez; istekleri karşılar ve servis katmanına devreder.
Çalıştırma: backend/ içinden  uvicorn app.main:app --reload
"""

from fastapi import FastAPI , HTTPException , Query
from app.schemas.schemas import YorumIstegi
from app.services.analysis_service import analyze_and_save , get_history , get_stats

app =FastAPI(
    title="Yorum analizi API",
    description="Türkçe müşteri yorumlarinin duygu analizi",
    version="0.1.0"

)
@app.get("/")
def kok():
    return {"message": "API çalışıyor."}

@app.post("/analysis")
#Yorumu Gemini'ye analiz ettirir, veritabanina kaydeder, sonucu doner.
async def analiz_et(istek:YorumIstegi):

    try:
        sonuc=await analyze_and_save(istek.comment)
    except ValueError as hata:
        raise HTTPException(status_code=502, detail=str(hata))
    return sonuc

@app.get("/analysis/history")
def gecmis(limit: int = Query(default=10, ge=1, le=100)):
    """Son analizleri listeler."""
    return get_history(limit)

@app.get("/analysis/stats")
def istatistikler():
    """Duygu dagilimini ve toplam analiz sayisini doner."""
    return get_stats()