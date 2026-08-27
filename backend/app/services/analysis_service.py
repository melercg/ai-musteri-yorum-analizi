"""
    Analiz sonuclarini veritabanina kaydeder.
"""

import asyncio

from app.db.database import get_connection
from app.services.gemini_service import analyze_comment


def save_analysis(comment: str, result: dict) -> int:
    """
        Bir analiz sonucunu veritabanina kaydeder.
        Kaydedilen satirin id'sini dondurur.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO analyses (comment, sentiment, confidence, explanation)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (comment, result["sentiment"], result["confidence"], result["explanation"]),
    )

    yeni_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()

    return yeni_id

def get_history(limit: int = 10) -> list:
    """Son analizleri yeniden eskiye dogru listeler."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, comment, sentiment, confidence, explanation, created_at
        FROM analyses
        ORDER BY id DESC
        LIMIT %s;
        """,
        (limit,),
    )

    kayitlar = cur.fetchall()

    cur.close()
    conn.close()

    return kayitlar

def get_stats() -> dict:
    """Duygu dagilimini ve toplam analiz sayisini doner."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sentiment, COUNT(*) AS adet
        FROM analyses
        GROUP BY sentiment
        ORDER BY adet DESC;
        """
    )

    satirlar = cur.fetchall()

    cur.close()
    conn.close()
    dagilim = {}
    for satir in satirlar:
      dagilim[satir["sentiment"]] = satir["adet"]
    return {"toplam": sum(dagilim.values()), "dagilim": dagilim}


async def analyze_and_save(comment: str) -> dict:
    """
    Yorumu Gemini'ye analiz ettirir, sonucu veritabanina kaydeder.
    Kaydin id'sini de icine koyup sonucu dondurur.'
        
    """
    result = await analyze_comment(comment)
    yeni_id = save_analysis(comment, result)
    result["id"] = yeni_id

    return result


if __name__ == "__main__":

    async def _main():
        comment = input("Analiz edilecek yorumu girin: ").strip()
        if not comment:
            print("Lütfen bir yorum girin.")
            return
        print("Analiz ediliyor...")
        sonuc = await analyze_and_save(comment)

        print(f"\nid       : {sonuc['id']}")
        print(f"Duygu    : {sonuc['sentiment']}")
        print(f"Guven    : %{int(sonuc['confidence'] * 100)}")
        print(f"Aciklama : {sonuc['explanation']}")

    asyncio.run(_main())
