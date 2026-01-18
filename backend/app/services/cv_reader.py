from pathlib import Path
import PyPDF2
from docx import Document

class CVReadError(Exception):
    pass

async def read_cv_from_file(file_path: str) -> str:

    path = Path(file_path)
    
    if not path.exists():
        raise CVReadError(f"Filen {file_path} finns inte")
    
    if path.suffix.lower() == ".pdf":
        return await _read_pdf(file_path)
    elif path.suffix.lower() in [".docx", ".doc"]:
        return await _read_docx(file_path)
    else:
        raise CVReadError(f"Filtypen {path.suffix} stöds inte. Använd PDF eller DOCX")

async def _read_pdf(file_path: str) -> str:
    try:
        text_content = []
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        return "\n".join(text_content)
    except Exception as e:
        raise CVReadError(f"Kunde inte läsa PDF: {str(e)}")

async def _read_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text_content = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_content.append(paragraph.text)
        return "\n".join(text_content)
    except Exception as e:
        raise CVReadError(f"Kunde inte läsa Word-dokument: {str(e)}")