# 🧊 Coolio - Smart Fridge App mit KI-Rezeptgenerator

Eine intelligente Kühlschrank-Verwaltungs-App mit integriertem KI-Rezeptgenerator.

## ✨ Features

- 📱 **PWA** - Progressive Web App für Mobile & Desktop
- 📷 **Barcode Scanner** - Scanne Produkte direkt mit der Kamera
- 🔍 **OpenFoodFacts Integration** - Automatische Produkterkennung
- 🤖 **KI-Rezeptgenerator** - Intelligente Rezepte basierend auf deinen Zutaten
- 👥 **Multi-User Support** - Mehrere Benutzer mit eigenen Kühlschränken
- 📅 **Ablaufdatum-Tracking** - Behalte den Überblick über deine Lebensmittel

## 🚀 Installation

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Google Gemini API Key einrichten (für KI-Rezepte)

Der KI-Rezeptgenerator verwendet die **kostenlose** Google Gemini API. So erhältst du deinen API Key:

1. Besuche [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Melde dich mit deinem Google-Account an
3. Klicke auf **"Get API Key"** → **"Create API Key"**
4. Wähle ein bestehendes Google Cloud Projekt oder erstelle ein neues
5. Kopiere den generierten API Key

### 3. API Key als Umgebungsvariable setzen

**Linux/Mac:**
```bash
export GEMINI_API_KEY="dein-api-key-hier"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=dein-api-key-hier
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="dein-api-key-hier"
```

**Permanent speichern (Linux/Mac):**
```bash
echo 'export GEMINI_API_KEY="dein-api-key-hier"' >> ~/.bashrc
source ~/.bashrc
```

### 4. App starten

```bash
python app.py
```

Die App läuft dann auf `http://localhost:8888`

## 🍳 KI-Rezeptgenerator verwenden

1. Logge dich ein (Standard: `admin` / `admin`)
2. Füge Produkte zu deinem Kühlschrank hinzu
3. Klicke auf den **"🤖 KI Rezept"** Button
4. Die KI analysiert deine Zutaten und generiert ein passendes, realistisches Rezept!

### Was macht der KI-Generator besonders?

- ✅ **Intelligente Zutatenkombination** - Kein "Salat mit Burger Buns"
- ✅ **Realistische Rezepte** - Nur kochbare, sinnvolle Gerichte
- ✅ **Kreativ & Praktisch** - Nutzt vorhandene Zutaten optimal
- ✅ **Kostenlos** - Google Gemini API ist im Free Tier kostenlos (60 Anfragen/Min)

## 📝 API Key Limits (Google Gemini Free Tier)

- **60 Anfragen pro Minute**
- **128.000 Tokens pro Minute**
- **Keine Kreditkarte erforderlich**
- **Völlig kostenlos**

## 🔧 Entwicklung

### Projekt-Struktur

```
.
├── app.py                      # Flask Backend
├── templates/
│   └── index.html             # Frontend (HTML + JS)
├── static/
│   ├── manifest.webmanifest   # PWA Manifest
│   └── service-worker.js      # Offline Support
├── produkte.json              # Produktdatenbank (per User)
├── users.json                 # Benutzerdatenbank
└── requirements.txt           # Python Dependencies
```

### Standard Login-Daten

- **Username:** `admin`
- **Password:** `admin`

## 📦 Dependencies

- **Flask** - Web Framework
- **requests** - HTTP Client für OpenFoodFacts API
- **google-generativeai** - Google Gemini AI SDK

## 🤝 Beitragen

Contributions sind willkommen! Öffne einfach ein Issue oder Pull Request.

## 📄 Lizenz

MIT License

## 🎯 Roadmap

- [ ] Export von Rezepten als PDF
- [ ] Einkaufslisten-Generator
- [ ] Ernährungswerte-Tracking
- [ ] Favoriten-Rezepte speichern
- [ ] Rezept-Bewertungssystem

---

**Erstellt mit ❤️ und KI**
