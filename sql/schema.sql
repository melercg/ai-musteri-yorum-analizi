-- Yorum analizi veritabani semasi
--
-- Kurulum:
--   createdb yorum_analizi
--   psql yorum_analizi -f sql/schema.sql

-- Gemini'nin analiz ettigi yorumlar ve sonuclari.
CREATE TABLE IF NOT EXISTS analyses (
    id          SERIAL PRIMARY KEY,
    comment     TEXT           NOT NULL,    -- analiz edilen yorum metni
    sentiment   VARCHAR(10)    NOT NULL,    -- pozitif / negatif / notr
    confidence  REAL           NOT NULL,    -- modelin guven skoru, 0-1 arasi
    explanation TEXT,                       -- modelin gerekcesi (bos olabilir)
    created_at  TIMESTAMP      DEFAULT NOW()
);
