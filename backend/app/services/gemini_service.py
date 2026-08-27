"""
YOL HARITAM:
   1.Gerekli kütüphane import et
   2.API key ile Gemini Client oluştur
   3.İlk basit mesajlaşmayı dene
   

KURULUM:

1.Virtual Environment oluşturup-aktifleştir:
   -python -m venv venv
   -source venv/bin/activate

2.requirements.txt dosyasına ekleme yap
    -google-genai
    -python-dotenv
   
3.Bağımlılıkları yükle:
    -pip install -r requirements.txt

4.Backend/ .env dosyasına API keyini ekle
    - GEMINI_API_KEY=YOUR_API_KEY
"""

import asyncio
import json
import sys
from google import genai
from app.core.config import GEMINI_API_KEY

#başarılı şekilde API key yuklendiyse, model seçimini yapalım.
# Hangi modeli kullanacağımızı seçtik ve Gemini'ye bağlanan client (istemci) nesnesini oluşturduk
MODEL_NAME= "gemini-3.6-flash"
client=genai.Client(api_key=GEMINI_API_KEY)


#İlk basit mesajlaşmayı dene ve GEMINI API bağlantısını test et 
# Bağlantı testi. Gemini'ye basit bir mesaj yollayıp cevabını ekrana basıyoruz. Amaç: "API anahtarım çalışıyor mu, bağlantı kuruluyor mu?" sorusunun cevabı.
async def first_message(message):
    response= await client.aio.models.generate_content(
        model=MODEL_NAME,
        contents=message
    )
    print(response.text)
    print()


def build_prompt(comment:str) -> str:
    """
    Yorumun duygu analizini yapacak promptu oluşturur.
    Args:
        comment (str): Analiz edilecek yorum
    Returns:
        str: Gemini'ye gönderilecek prompt
    """
    prompt= f"""
    Aşağıdaki yorumu analiz et ve duygu durumunu belirle. 
    Yorum: "{comment}"
    Cevabı JSON formatında ver.
    JSON formatı: {{
        "sentiment": "pozitif/negatif/nötr", 
        "confidence": 0-1 arası float,
        "explanation": "yorumun duygu durumunu belirleme gerekçesi"
        }}
    """
    return prompt.strip()


async def analyze_comment(comment:str) -> dict:
    # verilen yorumu async olarak analzi edip sentiment, confidence, explanation olarak return eden fonk yazalım.
    #raisses: ValueError: gemini gecerli bir json dönmezse diye

    prompt=build_prompt(comment)

    response= await client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
    )
# Gemini cevabı bazen ```json ... ``` bloğunun içine sarıyor. Temizle:
    raw_text=response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").strip()      # bastaki/sondaki backtickleri sil
        if raw_text.startswith("json"):             # kalan "json" etiketini sil
          raw_text = raw_text[4:].strip() 

    try:
        result=json.loads(raw_text)

    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini'den geçerli JSON alınamadı. Cevap: {raw_text}") from  e

    #beklenen keylerin cevabın içerde olup olmadığını kontrol et
    # Model bazen alan atlayabilir; eksikse burada dur, veritabanına bozuk kayıt gitmesin.
    required_keys={"sentiment","confidence","explanation"}
    if not required_keys.issubset(result.keys()):
        raise ValueError(f"Gemini cevabı beklenen keyleri içermiyor. Cevap: {result}")
    return result

#Standolene test: Bu dosya doğrudan çalışıtırılırsa yapacağı test 
async def _main():
    #Gemini' den cevap alana kadar bekle ,gelince alt satıra geç
    # await first_message("Merhaba Gemini, ben melisa") # test adımıydı
    #await first_message("duygu analizi projemde sana da yer veriyorum . Beni destekler misin?,  Duygu analizi nedir? 2 cümleyle anlat.") # test adımıydı 
    #print(build_prompt("Naber")) #test adıymıydı
    
    if len(sys.argv) >1:
        comment= " ".join(sys.argv[1:]) #komut satırından yorum al
    else:
        comment=input("Analiz edilecek yorumu girin: ").strip()
        if not comment:
            print("Lütfen bir yorum girin.") 
            sys.exit(1) 

    print(f"\nYorum:{comment}")
    print("Analiz ediliyor...")

    result=await analyze_comment(comment)
    print("\nAnaliz Sonucu:")
    print(f"Duygu: {result['sentiment']}")
    print(f"Güven: %{int(result['confidence']* 100)}")
    print(f"Açıklama: {result['explanation']}")

#Buradaki if aslında dosya doğrudan çalıştırıldıgında testi baslat . Ama baskası import ettiyse ,testi çalıştırma ,sadece fonk. kullansın .
if __name__ =="__main__":
    #async fonk çalıştırmak için asyncio.run(_main())
    asyncio.run(_main())
# Bu blok şu demek: "Bu dosya doğrudan çalıştırılırsa (python gemini_service.py) testi çalıştır. Ama başka bir dosya bunu import ederse çalıştırma."
#asyncio.run() de async fonksiyonu başlatmanın yolu — async fonksiyonlar direkt çağrılamaz. 
# Normal bır fonk çağırınca çalışır. 
#  Normal bir fonksiyon gibi çağırmak için asyncio.run() kullanıyoruz
#  Kritik nokta: asyncio.run() bir programda sadece bir kere çağrılır. 
# Bu yüzden async dünyaya giriş kapısıdır — "bir tane kapı, içerideistediğin kadar oda".

#-----------------------------------------------------------------------------------------------------------------------------


     


