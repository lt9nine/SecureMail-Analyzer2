# 🚀 Setup Guide - SecureMail Analyzer

## 📋 Voraussetzungen

### System-Anforderungen
- **Python 3.11+** (empfohlen: 3.13+)
- **Node.js 18+** (empfohlen: 18.19.0)
- **Git**
- **Code-Editor** (VS Code empfohlen)

### Python Installation
```bash
# Windows (mit winget)
winget install Python.Python.3.11

# Oder von python.org herunterladen
# https://www.python.org/downloads/
```

### Node.js Installation
```bash
# Windows (mit winget)
winget install OpenJS.NodeJS

# Oder von nodejs.org herunterladen
# https://nodejs.org/
```

## 🛠 Projekt-Setup

### 1. Repository klonen
```bash
git clone <repository-url>
cd SecureMail-Analyzer2
```

### 2. Backend Setup

#### Virtual Environment erstellen
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Dependencies installieren
```bash
pip install -r requirements.txt
```

#### Umgebungsvariablen konfigurieren
```bash
# .env Datei erstellen
cp .env.example .env
```

`.env` Datei bearbeiten:
```env
# Datenbank
DATABASE_URL=sqlite:///./securemail.db

# Sicherheit
SECRET_KEY=your-super-secret-key-change-this-in-production

# AI Provider
OPENROUTER_API_KEY=your-openrouter-api-key

# VirusTotal
VIRUSTOTAL_API_KEY=your-virustotal-api-key

# Debug
DEBUG=True
```

#### Datenbank initialisieren
```bash
# Alembic initialisieren (später)
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

#### Backend starten
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

#### Dependencies installieren
```bash
cd frontend
npm install
```

#### Frontend starten
```bash
npm run dev
```

## 🔑 API Keys Setup

### OpenRouter API Key
1. Gehe zu [openrouter.ai](https://openrouter.ai)
2. Registriere dich und erstelle einen API Key
3. Füge den Key in die `.env` Datei ein

### VirusTotal API Key
1. Gehe zu [virustotal.com](https://virustotal.com)
2. Registriere dich für einen kostenlosen API Key
3. Füge den Key in die `.env` Datei ein

## 🧪 Erste Schritte

### 1. Backend testen
```bash
# Health Check
curl http://localhost:8000/health

# API Docs
# Öffne http://localhost:8000/docs im Browser
```

### 2. Frontend testen
```bash
# Öffne http://localhost:5173 im Browser
```

### 3. Datenbank prüfen
```bash
# SQLite Datenbank sollte erstellt worden sein
ls backend/securemail.db
```

## 🔧 Entwicklung

### Backend Development
```bash
cd backend
# Virtual Environment aktivieren
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Mit Auto-Reload starten
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Tests ausführen
```bash
# Backend Tests
cd backend
pytest

# Frontend Tests
cd frontend
npm run test
```

## 📁 Projektstruktur verstehen

```
SecureMail-Analyzer2/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy Models
│   │   ├── services/       # Business Logic
│   │   ├── api/           # FastAPI Routes
│   │   ├── core/          # Config, Security
│   │   └── utils/         # Helper Functions
│   ├── alembic/           # Database Migrations
│   ├── tests/             # Backend Tests
│   └── main.py            # App Entry Point
├── frontend/               # Vue.js Frontend
│   ├── src/
│   │   ├── components/    # Vue Components
│   │   ├── views/         # Page Views
│   │   ├── stores/        # Pinia Stores
│   │   └── utils/         # Frontend Utils
│   └── package.json
└── docs/                  # Dokumentation
```

## 🚨 Troubleshooting

### Python Version Problem
```bash
# Python Version prüfen
python --version

# Sollte 3.11.x oder 3.13.x sein
```

### Node.js Version Problem
```bash
# Node.js Version prüfen
node --version

# Sollte 18.x.x sein
```

### Port bereits belegt
```bash
# Port 8000 prüfen (Windows)
netstat -ano | findstr :8000

# Port 5173 prüfen
netstat -ano | findstr :5173
```

### Virtual Environment Problem
```bash
# Virtual Environment neu erstellen
rm -rf venv
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 📚 Nächste Schritte

1. **Datenbank-Models implementieren**
2. **Authentifizierung einrichten**
3. **IMAP-Integration entwickeln**
4. **Mail-Analyse-Pipeline aufbauen**
5. **Frontend-Komponenten erstellen**

## 🔗 Nützliche Links

- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [Vue.js Dokumentation](https://vuejs.org/)
- [SQLAlchemy Dokumentation](https://docs.sqlalchemy.org/)
- [PrimeVue Komponenten](https://primevue.org/) 