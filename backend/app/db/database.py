"""
PostgreSQL bağlantısı (Raw SQL - psycopg2).

ORM (SQLAlchemy) bilinçli olarak kullanılmadı: sorgular basit
(INSERT, SELECT ... LIMIT, GROUP BY) ve projenin amacı SQL'i doğrudan görmek.
Her fonksiyon kendi bağlantısını açıp kapatır — bağlantı havuzu (pool) yok,
bu ölçekte gerekmiyor.

Test: backend/ içinden  python -m app.db.database
"""


import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import DATABASE_URL


def get_connection():
  """Veritabanina yeni bir baglanti acar."""
  return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


# Standalone test                                                                                                     
if __name__ == "__main__":
  conn = get_connection()
  cur = conn.cursor()

  cur.execute("SELECT COUNT(*) AS adet FROM analyses;")
  print("Baglanti OK. Kayit sayisi:", cur.fetchone()["adet"])

  cur.close()
  conn.close()