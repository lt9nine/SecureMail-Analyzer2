# 🔐 Projektplan: E-Mail-Sicherheitsanalyse mit Web-Frontend und KI

## 🎯 Ziel des Projekts

Ein sicheres, webbasiertes Tool für technisch versierte Nutzer:innen, das per IMAP auf mehrere Mailkonten zugreift, eingehende Mails analysiert (Spam, Phishing, Malware etc.), diese in Gefahrenstufen einteilt und als durchsuchbare, lesbare Daten im Frontend anzeigt. Es unterstützt mehrere Nutzer mit jeweils mehreren IMAP-Konten (Mandantentrennung) und kann Mails auch direkt über das Frontend löschen oder anzeigen.

---

## 📦 Modulübersicht

### 1. Benutzer- & Kontenverwaltung

- Nutzer-Accounts (Registrierung, Login, JWT)
- Mandantentrennung (jeder Nutzer hat mehrere IMAP-Konten)
- Verwaltung von IMAP-Zugangsdaten im verschlüsselten Backend (z. B. `cryptography`)

---

### 2. IMAP-Fetcher & Mail-Synchronisierung

- Läuft regelmäßig oder dauerhaft im Hintergrund (z. B. Celery/Async Job)
- Verbindet sich zu IMAP-Konten aller Nutzer
- Für jedes Konto:
  - Lädt neue Mails (vergleicht UIDs mit zuletzt bekanntem Stand)
  - Prüft auf gelöschte Mails → markiert in DB
  - Führt ggf. Umbennenung der Mails durch (`rename_subject`)
  - Übergibt neue Mails an die Analyse-Pipeline

---

### 3. Analyse-Pipeline (umfangreich, modular, prüfbar per Python)

#### 🔍 Metadaten-Checks

- Absendervertrauen (DKIM/SPF/DMARC via `auth_headers`)
- Absenderadresse vs. angezeigter Name
- Betreffmuster-Analyse (Verdachtstexte)
- Domain-Prüfung (z. B. `paypal.support@fake.com`)
- Reply-To abweichend?

#### 📎 Header-Checks

- Received-Header-Kette analysieren (z. B. Serverumleitung)
- Manipulation von Mailpfad

#### 📄 Inhaltsprüfung

- HTML-Inhalt entschärfen (kein JS, keine Inline-Bilder)
- Link-Ziel und Link-Text Vergleich
- Schwarze Liste von Wörtern / Marken
- Script-Injection verhindern

#### 📎 Anhangsanalyse

- MIME-Typ-Validierung
- Dateityp-Abgleich (z. B. `.pdf` mit MIME-Check)
- SHA256-Signatur, evtl. VT-API
- Kein aktives Öffnen

#### 🤖 KI-gestützte Analyse

- Modell wählbar:
  - Remote (OpenRouter, z. B. GPT-4, Claude, Mistral)
  - Lokal (Ollama mit LLaMA3 oder TinyLLM)
- Check per Prompt:
  - „Wie wahrscheinlich ist es, dass diese Mail Phishing ist?“
  - Antworten mit Confidence + Erklärung

#### 📊 Ergebnis-Zusammenfassung

- Gefahrenstufe (Low / Medium / High / Critical)
- Risikogründe (z. B. "Absender-Domain verdächtig", "Anhänge mit potenzieller Malware")

---

### 4. Datenbankmodell (PostgreSQL / SQLite / andere)

```python
class User(Base):
    id, email, password_hash, settings

class MailAccount(Base):
    id, user_id, email, imap_host, imap_port, encrypted_password

class Email(Base):
    id, mail_account_id
    subject, from_addr, to_addr, date
    content_plain, content_html, attachments
    uid_original, uid_current
    is_deleted, is_read
    analysis_score, risk_level, analysis_details
    created_at, updated_at, deleted_at

class Attachment(Base):
    id, email_id
    filename, mime_type, sha256, is_suspicious
```

---

### 5. Frontend (Vue / React, REST-API)

#### 📬 Mailübersicht

- Liste aller nicht-gelöschten Mails
- Filter nach Risiko, Konto, Zeitraum
- Ampelanzeige für Gefahrenstufe
- Suche nach Betreff/Absender

#### 📖 Detailansicht

- HTML/Plaintext-Anzeige (safe)
- Link-Liste mit Ziel
- Anhangliste mit Typ/Risiko
- Analyse-Zusammenfassung
- Aktionen:
  - Mail löschen (→ Backend löscht in IMAP)
  - Als sicher markieren
  - Original anzeigen

---

### 6. Mail-Löschung & Konsistenz

#### 🗑 Wenn Benutzer im Frontend löscht:

- API → Backend → IMAP:
  - Setzt `\Deleted` Flag → `EXPUNGE`
  - Aktualisiert DB: `is_deleted = True`, `deleted_at = timestamp`

#### ❌ Wenn Mail extern gelöscht wurde:

- UID nicht mehr vorhanden beim nächsten Sync → Flag in DB setzen
- Keine Hard-Deletion für Nachverfolgbarkeit

---

### 7. Technologien / Empfehlungen

| Bereich              | Tool/Lib           |
|----------------------|--------------------|
| Backend              | FastAPI oder Flask |
| IMAP                 | `imap-tools`, `imaplib` |
| HTML Sanitizing      | `bleach`, `html2text` |
| DB ORM               | SQLAlchemy         |
| KI-Anbindung         | OpenRouter, Ollama |
| Frontend             | React oder Vue.js  |
| Job Queue (optional) | Celery, APScheduler |
| Sicherheit           | TLS, OAuth, AES PW Store |

---

### 8. Skalierung & Zukunft

- Datenbank modular, leicht zu migrieren (PostgreSQL bevorzugt)
- Microservice-Fähigkeit durch getrennte Analyse-, IMAP- und API-Module
- Frontend + DB können über WebSocket oder Polling synchronisiert werden
- Erweiterbar um:
  - Webhook bei neuer High-Risk-Mail
  - Mail-Weiterleitung an Postfächer (z. B. Sicherheitsadmin)
  - Benutzer-Rollenverwaltung (Audit-Only)

---

## 🛠 Nächste Meilensteine

| Schritt | Aufgabe |
|--------|--------|
| ✅ 1 | Benutzerverwaltung + Mailkonten-Anbindung |
| ✅ 2 | IMAP-Sync (Neues & Gelöschtes erkennen) |
| ✅ 3 | Analyse-Pipeline implementieren |
| ⏳ 4 | Analyse-Ergebnisse in DB speichern |
| ⏳ 5 | Frontend Mail-Übersicht & Detailansicht |
| ⏳ 6 | Mail-Viewer mit entschärfter HTML-Ausgabe |
| ⏳ 7 | Anhangsanalyse einbinden |
| ⏳ 8 | Mail-Löschung vom Frontend |
| ⏳ 9 | Auswahl des KI-Backends im User-Interface |
| 🔜 10 | Deployment-Dockerisierung & Configs |
