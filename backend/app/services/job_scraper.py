import requests
from bs4 import BeautifulSoup
import asyncio

async def scrape_job_posting(url: str) -> str:
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.get(url, timeout=10.0)
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        raise Exception(f"Kunde inte hämta jobbannons från URL: {str(e)}")

