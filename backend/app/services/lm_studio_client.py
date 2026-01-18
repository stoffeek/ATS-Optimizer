import asyncio  # Används för att köra blocking I/O asynkront
import requests  # Används för HTTP-anrop till LM Studio
from app.services import keyword_extractor  # Används för att begränsa tillåtna keywords

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"  # OpenAI-kompatibel endpoint i LM Studio
LM_STUDIO_MODEL = "meta-llama-3.1-8b-instruct"  # Modell-id från LM Studio API Usage

async def optimize_cv(cv_text: str, job_text: str) -> str:  # Optimerar CV med hjälp av LM Studio
    allowed_keywords = keyword_extractor.extract_keywords(cv_text, top_n=80)  # Hämtar tillåtna ord från CV:t
    allowed_text = ", ".join(allowed_keywords)  # Skapar en kommaseparerad lista för prompten
    system_prompt = "Du är en professionell CV-optimerare som skriver ATS-vänliga CV:n."  # Systeminstruktion för modellen
    user_prompt = (  # Bygger användarprompt med både CV och jobbannons
        "Optimera detta CV för jobbannonsen nedan och gör det välskrivet, professionellt och ATS-vänligt. "  # Anger mål för kvalitet
        "Behåll exakt samma sektioner, rubriker och ordning som i CV:t. "  # Tvingar samma struktur
        "Skriv ENDAST om formuleringar för bättre flyt, stavning och tydlighet. "  # Tillåter förbättring utan förändring av fakta
        "Skapa INTE nya namn, företag, datum, titlar eller erfarenheter. "  # Förbjuder påhittad information
        "Lägg INTE till nya tekniker som saknas i CV:t. "  # Förhindrar stack-byte
        "Skriv INTE placeholders som [Inget ...]. "  # Förbjuder placeholder-text
        "Behåll språk per sektion (översätt inte mellan svenska/engelska). "  # Låser språket
        "Använd keywords från jobbannonsen endast om de redan finns i CV:t. "  # Hindrar att nya ord läggs till
        f"Tillåtna keywords från CV:t: {allowed_text}. "  # Ger explicit lista över tillåtna ord
        "Skapa TVÅ versioner av CV:t: först svenska, sedan engelska. "  # Kräver dubbel output
        "Format: börja med raden '=== SVENSKA CV ===' och därefter '=== ENGLISH CV ==='. "  # Tydliga markörer för versioner
        "Returnera ENDAST text utan markdown. "  # Kräver ren text utan markdown
        "Rubriker ska avslutas med ':' och bullets ska börja med '- '.\n\n"  # Standardiserar format för DOCX
        f"JOBBANNONS:\n{job_text}\n\n"  # Lägger in jobbannonsens text
        f"CV:\n{cv_text}\n"  # Lägger in CV-texten
    )  # Slut på prompten
    payload = {  # Skapar payload för OpenAI-kompatibel chat/completions
        "model": LM_STUDIO_MODEL,  # Väljer modellen i LM Studio
        "messages": [  # Skapar meddelandelista för chat-formatet
            {"role": "system", "content": system_prompt},  # Systemmeddelande för modellens beteende
            {"role": "user", "content": user_prompt},  # Användarmeddelande med uppgiften
        ],  # Slut på meddelandelistan
        "temperature": 0.1,  # Lägre temperatur för mer konsekvent output
    }  # Slut på payload
    loop = asyncio.get_event_loop()  # Hämtar event loop för async I/O
    response = await loop.run_in_executor(  # Kör blocking requests i separat tråd
        None,  # Använder default threadpool
        lambda: requests.post(LM_STUDIO_URL, json=payload, timeout=120.0),  # Skickar POST-anrop till LM Studio
    )  # Slut på async körning
    response.raise_for_status()  # Kastar fel om HTTP-status inte är OK
    data = response.json()  # Tolkar JSON-svaret
    content = data["choices"][0]["message"]["content"]  # Plockar ut textsvaret från modellen
    return content  # Returnerar den optimerade CV-texten

