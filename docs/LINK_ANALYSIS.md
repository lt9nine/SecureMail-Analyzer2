# 🔗 Link-Sicherheitsanalyse

## 📋 Übersicht

Die Link-Analyse ist ein zentraler Bestandteil der E-Mail-Sicherheitsanalyse und erkennt verschiedene Arten von verdächtigen URLs und Phishing-Links.

## 🎯 Erkannte Bedrohungen

### 1. **Lookalike-Domains**
- **Erkennung**: Fuzzy-String-Matching mit 70-80% Ähnlichkeit
- **Beispiele**: 
  - `g00gle.com` → `google.com`
  - `paypa1.com` → `paypal.com`
  - `micros0ft.com` → `microsoft.com`
- **Score**: +40 Punkte

### 2. **Phishing-Keywords in URLs**
- **Erkannte Keywords**:
  - `login`, `signin`, `secure`, `verify`, `confirm`
  - `account`, `password`, `security`, `banking`
  - `urgent`, `immediate`, `action`, `required`
  - `suspended`, `compromised`, `hacked`, `breach`
- **Score**: +15 Punkte

### 3. **URL-Shortener**
- **Erkannte Services**:
  - `bit.ly`, `tinyurl.com`, `goo.gl`, `t.co`
  - `is.gd`, `v.gd`, `ow.ly`, `su.pr`
  - `twurl.nl`, `snipurl.com`, `short.to`
- **Score**: +25 Punkte

### 4. **IP-Adressen statt Domains**
- **Erkennung**: IPv4-Adressen in URLs
- **Beispiel**: `http://192.168.1.100/login`
- **Score**: +30 Punkte

### 5. **Text-URL-Mismatch**
- **Erkennung**: Link-Text stimmt nicht mit Ziel-URL überein
- **Beispiel**: `<a href="https://evil.com">https://google.com</a>`
- **Score**: +35 Punkte

### 6. **Nicht-HTTPS Verbindungen**
- **Erkennung**: HTTP statt HTTPS
- **Score**: +10 Punkte

### 7. **Verdächtige TLDs**
- **Erkannte TLDs**:
  - `.tk`, `.ml`, `.ga`, `.cf`, `.gq` (kostenlose TLDs)
  - `.xyz`, `.top`, `.club`, `.online` (günstige TLDs)
- **Score**: +20 Punkte

### 8. **Verdächtige Subdomains**
- **Erkannte Subdomains**:
  - `secure`, `login`, `signin`, `verify`
  - `account`, `password`, `security`, `banking`
- **Score**: +20 Punkte

## 🛠 Technische Implementierung

### Backend-Service: `LinkAnalyzer`

```python
from app.services.link_analyzer import LinkAnalyzer

# Initialisierung
link_analyzer = LinkAnalyzer()

# Analyse durchführen
result = link_analyzer.analyze_links(html_content, plain_text)
```

### Verwendete Python-Module

| Modul | Zweck | Version |
|-------|-------|---------|
| `tldextract` | Domain-Extraktion | 5.1.1 |
| `dnspython` | DNS-Lookups | 2.6.1 |
| `fuzzywuzzy` | String-Ähnlichkeit | 0.18.0 |
| `validators` | URL-Validierung | 0.22.0 |
| `url-normalize` | URL-Normalisierung | 1.4.3 |

### Konfiguration

```python
# backend/app/services/link_analyzer.py

class LinkAnalyzer:
    def __init__(self):
        # Legitime Domains (erweiterbar)
        self.legitimate_domains = {
            'google.com', 'gmail.com', 'microsoft.com',
            'paypal.com', 'amazon.com', 'facebook.com'
        }
        
        # Verdächtige TLDs (erweiterbar)
        self.suspicious_tlds = {
            '.tk', '.ml', '.ga', '.cf', '.gq',
            '.xyz', '.top', '.club', '.online'
        }
        
        # Phishing-Keywords (erweiterbar)
        self.phishing_keywords = {
            'login', 'signin', 'secure', 'verify',
            'account', 'password', 'urgent', 'immediate'
        }
```

## 📊 Risiko-Bewertung

### Score-Berechnung
- **0-29 Punkte**: Safe (grün)
- **30-59 Punkte**: Warning (gelb)
- **60-79 Punkte**: Danger (rot)
- **80-100 Punkte**: Critical (dunkelrot)

### Gewichtung
- **Kritisch**: Lookalike-Domains, IP-Adressen, Text-Mismatch
- **Hoch**: URL-Shortener, verdächtige Subdomains
- **Mittel**: Phishing-Keywords, verdächtige TLDs
- **Niedrig**: Nicht-HTTPS

## 🎨 Frontend-Integration

### E-Mail-Details
- **Detaillierte Link-Analyse** mit allen gefundenen Links
- **Einzelne Bedrohungsanzeige** pro Link
- **Score-Anzeige** und Status-Indikatoren
- **Klickbare URLs** (öffnen in neuem Tab)

### E-Mail-Liste
- **Kompakte Indikatoren** für verdächtige Links
- **Tooltips** mit Erklärungen
- **Score-Anzeige** in der Vorschau

### CSS-Klassen
```css
.link-status.safe { background: #d4edda; color: #155724; }
.link-status.warning { background: #fff3cd; color: #856404; }
.link-status.danger { background: #f8d7da; color: #721c24; }
.link-status.critical { background: #f5c6cb; color: #721c24; }
```

## 🔧 Erweiterbarkeit

### Neue Bedrohungstypen hinzufügen

1. **Bedrohung definieren**:
```python
def _check_new_threat(self, url: str) -> Dict:
    # Implementierung
    return {
        'is_threat': True,
        'score': 25,
        'details': ['Neue Bedrohung erkannt']
    }
```

2. **In Analyse integrieren**:
```python
# In _analyze_single_link()
new_threat = self._check_new_threat(url)
if new_threat['is_threat']:
    threats.append('new_threat')
    details.extend(new_threat['details'])
    score += new_threat['score']
```

3. **Frontend erweitern**:
```javascript
getThreatText(threat) {
  const texts = {
    // ... bestehende ...
    new_threat: 'Neue Bedrohung erkannt'
  }
  return texts[threat] || threat
}
```

### Konfiguration erweitern

```python
# Neue legitime Domains
self.legitimate_domains.add('neue-domain.com')

# Neue verdächtige TLDs
self.suspicious_tlds.add('.suspicious')

# Neue Phishing-Keywords
self.phishing_keywords.add('neues_keyword')
```

## 🧪 Tests

### Unit Tests
```python
def test_lookalike_detection():
    analyzer = LinkAnalyzer()
    result = analyzer._check_lookalike_domain('g00gle.com')
    assert result['is_lookalike'] == True
    assert result['original'] == 'google'

def test_phishing_keywords():
    analyzer = LinkAnalyzer()
    keywords = analyzer._check_phishing_keywords('https://evil.com/login')
    assert 'login' in keywords
```

### Integration Tests
```python
def test_full_link_analysis():
    analyzer = LinkAnalyzer()
    html = '<a href="https://g00gle.com/login">Google Login</a>'
    result = analyzer.analyze_links(html, '')
    assert result['status'] == 'critical'
    assert len(result['links']) == 1
```

## 📈 Performance

### Optimierungen
- **Regex-Patterns** vorcompiliert
- **Domain-Cache** für wiederholte Lookups
- **Fuzzy-Matching** mit Schwellenwerten
- **Batch-Verarbeitung** für mehrere Links

### Benchmarks
- **Einzelner Link**: ~5ms
- **E-Mail mit 10 Links**: ~50ms
- **100 E-Mails**: ~5s

## 🔒 Sicherheitsaspekte

### URL-Sanitization
- **Keine direkten Redirects** zu verdächtigen URLs
- **Links öffnen** in neuem Tab mit `rel="noopener noreferrer"`
- **URL-Validierung** vor Analyse

### Datenschutz
- **Keine URL-Inhalte** an externe APIs gesendet
- **Lokale Analyse** ohne Netzwerk-Requests
- **Logging** nur für Debug-Zwecke

## 🚀 Zukünftige Erweiterungen

### Geplante Features
- **DNS-Blacklist-Check** (Spamhaus, etc.)
- **Reputation-Services** (Google Safe Browsing API)
- **Machine Learning** für bessere Erkennung
- **Real-time Updates** von Bedrohungsdaten

### API-Integrationen
- **VirusTotal URL API** für zusätzliche Checks
- **PhishTank API** für bekannte Phishing-URLs
- **URLVoid API** für Domain-Reputation 