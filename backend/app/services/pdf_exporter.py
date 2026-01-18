from reportlab.lib.pagesizes import A4  # Importerar standardformat A4 för PDF
from reportlab.pdfgen import canvas  # Importerar canvas för att rita text i PDF
from reportlab.lib.units import mm  # Importerar mm för enklare marginaler
from typing import List  # Importerar List för typangivelser

def _wrap_text(text: str, max_chars: int) -> List[str]:  # Radbryter texten för PDF
    lines: List[str] = []  # Skapar lista för rader
    for paragraph in text.splitlines():  # Itererar genom varje rad i input
        if not paragraph.strip():  # Om raden är tom
            lines.append("")  # Lägg in tom rad för luft
            continue  # Gå vidare till nästa rad
        words = paragraph.split()  # Dela upp raden i ord
        current = ""  # Håller pågående rad
        for word in words:  # Itererar genom orden
            test_line = f"{current} {word}".strip()  # Testar om ordet får plats
            if len(test_line) <= max_chars:  # Om raden inte blir för lång
                current = test_line  # Uppdaterar aktuell rad
            else:  # Om raden blir för lång
                lines.append(current)  # Lägg till raden
                current = word  # Starta ny rad med ordet
        if current:  # Om det finns kvar text i raden
            lines.append(current)  # Lägg till sista raden
    return lines  # Returnerar alla rader

def create_pdf_from_text(text: str, output_path: str) -> None:  # Skapar PDF från text
    width, height = A4  # Sätter sidstorlek till A4
    margin = 15 * mm  # Sätter marginaler
    line_height = 12  # Sätter radavstånd
    max_chars = 95  # Grov gräns för radlängd
    c = canvas.Canvas(output_path, pagesize=A4)  # Skapar PDF-canvas
    c.setFont("Helvetica", 10)  # Sätter standardfont
    y = height - margin  # Startposition från toppen
    lines = _wrap_text(text, max_chars)  # Radbryter texten
    for line in lines:  # Itererar genom alla rader
        if y < margin:  # Om vi når botten
            c.showPage()  # Skapar ny sida
            c.setFont("Helvetica", 10)  # Sätter font igen
            y = height - margin  # Återställ y-position
        c.drawString(margin, y, line)  # Ritar raden
        y -= line_height  # Flyttar y-positionen nedåt
    c.save()  # Sparar PDF-filen

