# 🔐 SecureMail-Analyzer2

Ein sicheres, webbasiertes Tool für E-Mail-Sicherheitsanalyse mit KI-gestützter Bedrohungserkennung.

## 🎯 Features

- **Multi-IMAP-Support**: Mehrere Mailkonten pro Nutzer
- **KI-gestützte Analyse**: OpenRouter API + lokale LLM-Unterstützung
- **Sicherheitsanalyse**: Spam, Phishing, Malware-Erkennung
- **Mandantentrennung**: Jeder Nutzer sieht nur seine eigenen Mails
- **Admin-Dashboard**: Vorfälle ohne Mail-Inhalt einsehbar
- **VirusTotal-Integration**: Anhangsanalyse mit VT API

## 🏗 Architektur

- **Backend**: FastAPI + SQLAlchemy + SQLite/PostgreSQL
- **Frontend**: Vue.js 3 + Vite
- **Authentifizierung**: JWT mit Refresh-Tokens
- **Datenbank**: SQLite (entwicklungsfreundlich) → PostgreSQL (produktionsbereit)
- **Mail-Sync**: APScheduler (5-Min-Intervalle)
- **Verschlüsselung**: AES-256-GCM für sensible Daten

## 📋 Voraussetzungen

- Python 3.11+ (empfohlen: 3.13+)
- Node.js 18+
- Git

## 🚀 Installation

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Umgebungsvariablen
```bash
# .env im Backend-Verzeichnis
DATABASE_URL=sqlite:///./securemail.db
SECRET_KEY=your-secret-key-here
OPENROUTER_API_KEY=your-openrouter-key
VIRUSTOTAL_API_KEY=your-vt-key
```

## 🏃‍♂️ Entwicklung starten

### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## 📁 Projektstruktur

```
SecureMail-Analyzer2/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy Models
│   │   ├── services/        # Business Logic
│   │   ├── api/            # FastAPI Routes
│   │   ├── core/           # Config, Security
│   │   └── utils/          # Helper Functions
│   ├── alembic/            # Database Migrations
│   ├── tests/              # Backend Tests
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue Components
│   │   ├── views/          # Page Views
│   │   ├── stores/         # Pinia Stores
│   │   └── utils/          # Frontend Utils
│   ├── public/
│   └── package.json
├── docs/                   # Dokumentation
└── README.md
```

## 🔧 Konfiguration

### Datenbank-Umschaltung
```python
# backend/app/core/config.py
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./securemail.db")
# Für PostgreSQL: postgresql://user:pass@localhost/securemail
```

### KI-Backend
```python
# Standard: OpenRouter API
AI_PROVIDER = "openrouter"  # oder "ollama" für lokales LLM
```

## 🧪 Tests

```bash
# Backend Tests
cd backend
pytest

# Frontend Tests
cd frontend
npm run test
```

## 📦 Deployment

### Docker (später)
```bash
docker-compose up -d
```

### Pterodactyl Egg (später)
- Node.js Egg für Frontend
- Python Egg für Backend
- PostgreSQL Egg für Datenbank

## 🔒 Sicherheit

- JWT-Token mit kurzer Lebensdauer
- Refresh-Token-Rotation
- AES-256-GCM für IMAP-Passwörter
- HTML-Sanitization für Mail-Inhalte
- Rate-Limiting für API-Endpoints
- CORS-Konfiguration

## 📝 Entwicklung

### Git Workflow (zukünftig)
- `main`: Produktionscode
- `develop`: Entwicklungsbranch
- `feature/*`: Feature-Branches
- `hotfix/*`: Dringende Fixes

## 🤝 Contributing

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## 📄 Lizenz

[Lizenz hier einfügen] 