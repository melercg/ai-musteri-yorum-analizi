"""
API'ye gelen verilerin şekli.

Pydantic bu tanımlara bakıp gelen JSON'u doğrular; uymuyorsa FastAPI
isteği 422 ile geri çevirir ve fonksiyon hiç çalışmaz.

Not: dönen cevabın şeması (response_model) henüz yok, sonra eklenecek.
"""

from pydantic import BaseModel, Field


class YorumIstegi(BaseModel):
    """POST /analysis gövdesi."""

    # min_length=1: boş yorum Gemini'ye hiç gitmesin, kota harcanmasın.
    # max_length=2000: aşırı uzun metin hem maliyet hem zaman aşımı riski.
    comment: str = Field(
        min_length=1,                                                                                                                                                                                         
        max_length=2000,
        description="Analiz edilecek müşteri yorumu",
    )
