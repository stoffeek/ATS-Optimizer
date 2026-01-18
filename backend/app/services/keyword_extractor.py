import re  # Regex för att rensa text från specialtecken
from collections import Counter  # Räknar förekomster av ord
from typing import List, Dict  # Typangivelser för tydlighet

STOPWORDS = {  # Vanliga ord som inte säger något om kompetenser
    "och", "att", "det", "som", "för", "med", "på", "är", "av", "en", "ett", "i", "till", "vi",  # Svenska stoppord
    "the", "and", "or", "to", "of", "in", "for", "with", "a", "an", "is", "are", "as", "on", "by",  # Engelska stoppord
}  # Slut på stopwords

def normalize_text(text: str) -> List[str]:  # Normaliserar text till en lista med relevanta ord
    cleaned = text.lower()  # Gör texten gemener för jämförelse
    cleaned = re.sub(r"[^a-zåäö0-9]+", " ", cleaned)  # Tar bort specialtecken och behåller ord
    words = cleaned.split()  # Delar upp texten i ord
    words = [word for word in words if len(word) >= 3 and word not in STOPWORDS]  # Filtrerar bort korta/stoppord
    return words  # Returnerar listan med normaliserade ord

def extract_keywords(text: str, top_n: int = 30) -> List[str]:  # Extraherar de vanligaste orden
    words = normalize_text(text)  # Rensar texten till ord
    counts = Counter(words)  # Räknar hur ofta varje ord förekommer
    most_common = counts.most_common(top_n)  # Tar ut de vanligaste orden
    keywords = [word for word, _ in most_common]  # Plockar ut endast orden
    return keywords  # Returnerar listan med keywords

def compare_keywords(job_text: str, cv_text: str, top_n: int = 30) -> Dict[str, List[str]]:  # Jämför keywords mellan jobb och CV
    job_keywords = extract_keywords(job_text, top_n)  # Keywords från jobbannons
    cv_keywords = extract_keywords(cv_text, top_n)  # Keywords från CV
    job_set = set(job_keywords)  # Gör set för snabb jämförelse
    cv_set = set(cv_keywords)  # Gör set för snabb jämförelse
    matched = sorted(list(job_set & cv_set))  # Ord som finns i båda
    missing = sorted(list(job_set - cv_set))  # Ord som saknas i CV
    return {  # Returnerar strukturerat resultat
        "job_keywords": job_keywords,  # Keywords från jobbannons
        "cv_keywords": cv_keywords,  # Keywords från CV
        "matched": matched,  # Gemensamma ord
        "missing": missing,  # Ord som saknas i CV
    }  # Slut på resultat

