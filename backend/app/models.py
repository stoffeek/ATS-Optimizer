from typing import Optional  # Används för att markera valfria fält i modeller
from pydantic import BaseModel  # Bas-klass för validering av JSON-kroppar

class JobPostingInput(BaseModel):  # Modell för jobbannons-input via API
    text: Optional[str] = None  # Jobbannons som ren text (valfri)
    url: Optional[str] = None  # Jobbannons-URL som ska hämtas (valfri)

class KeywordRequest(BaseModel):  # Modell för keyword-analys input
    job_text: Optional[str] = None  # Jobbannonsens text om den skickas direkt
    cv_text: Optional[str] = None  # CV-text om den skickas direkt
    top_n: int = 30  # Antal keywords som ska extraheras

class OptimizeRequest(BaseModel):  # Modell för CV-optimering med AI
    job_text: Optional[str] = None  # Jobbannonsens text om den skickas direkt
    cv_text: Optional[str] = None  # CV-text om den skickas direkt

