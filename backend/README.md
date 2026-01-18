# CV Optimizer Backend

## Snabbstart

### Starta servern

**PowerShell:**
```powershell
.\start.ps1
```

**Command Prompt (cmd):**
```cmd
start.bat
```

**Eller manuellt:**
```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

## Installation

1. Skapa virtuell miljö: `python -m venv venv`
2. Aktivera venv: `.\venv\Scripts\Activate.ps1`
3. Installera paket: `python -m pip install -r requirements.txt`

## API Endpoints

- `http://localhost:8000` - Root endpoint
- `http://localhost:8000/health` - Health check


