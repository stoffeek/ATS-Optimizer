from pathlib import Path
import os
import asyncio

DATA_DIR = Path(__file__).parent.parent.parent / "data"
MASTER_CV_FILE = DATA_DIR / "master_cv.txt"
JOB_POSTING_FILE = DATA_DIR / "job_posting.txt"

def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)

async def save_master_cv(cv_text: str) -> str:
    ensure_data_dir()
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: MASTER_CV_FILE.write_text(cv_text, encoding="utf-8"))
    return str(MASTER_CV_FILE)

def get_master_cv() -> str:
    if not MASTER_CV_FILE.exists():
        return ""
    with open(MASTER_CV_FILE, "r", encoding="utf-8") as f:
        return f.read()

async def save_job_posting(job_text: str) -> str:
    ensure_data_dir()
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: JOB_POSTING_FILE.write_text(job_text, encoding="utf-8"))
    return str(JOB_POSTING_FILE)

def get_job_posting() -> str:
    if not JOB_POSTING_FILE.exists():
        return ""
    with open(JOB_POSTING_FILE, "r", encoding="utf-8") as f:
        return f.read()

