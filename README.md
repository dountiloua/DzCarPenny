<p align="center">
  <img src="https://img.shields.io/badge/🚗-AUTO%20CAR%20SOURCER%20DZ-red?style=for-the-badge&labelColor=1a1a2e" alt="AUTO CAR SOURCER DZ">
</p>

<h1 align="center">AUTO CAR SOURCER DZ</h1>

<p align="center">
  <strong>AI-Powered Automotive Sourcing Agent for the French Used Car Market</strong><br>
  <em>Multi-platform search engine with smart filtering for export-ready vehicles</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/platforms-AutoScout24%20%7C%20Leboncoin%20%7C%20LaCentrale-blue?style=flat-square" alt="Platforms">
  <img src="https://img.shields.io/badge/status-production-brightgreen?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/deploy-Railway-purple?style=flat-square" alt="Deploy">
</p>

---

## 🎯 What Is AUTO CAR SOURCER DZ?

**AUTO CAR SOURCER DZ** is an intelligent automotive sourcing agent designed for professionals and individuals who source used vehicles from the French market for export. Instead of manually checking multiple platforms and applying filters repeatedly, this agent:

- Searches **3 major French platforms simultaneously** (AutoScout24, Leboncoin, LaCentrale)
- Applies **smart filters** automatically (fuel type, year range, accident-free, price cap)
- Generates **pre-filtered direct links** — click and see results instantly
- Runs as a **Telegram agent** for on-the-go sourcing from your phone
- Focuses on **export-ready vehicles** (non-accidenté, proper documentation)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 Multi-Platform Search | Simultaneously queries AutoScout24.fr, Leboncoin.fr, and LaCentrale.fr |
| ⛽ Smart Fuel Filter | Gasoline & Hybrid only — no diesel, no full electric |
| 📅 Dynamic Date Logic | Automatically calculates valid year range (current year - 3 + 2 months lead) |
| 🛡️ Condition Filter | Strictly non-accidenté (no accident history) vehicles |
| 💰 Price Cap | User-defined maximum budget in EUR (HT for export) |
| 🔗 Direct Links | Pre-filtered URLs — one click to view all matching listings |
| 📱 Telegram Interface | Search from anywhere via Telegram bot |
| 🚀 Instant Results | No scraping delays — generates optimized search URLs in seconds |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              AUTO CAR SOURCER DZ — AGENT                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌──────────────────────────────┐    │
│  │   Telegram  │    │       Search Engine          │    │
│  │   Interface │───►│  (URL Builder + Filters)     │    │
│  └─────────────┘    └──────────────┬───────────────┘    │
│                                    │                    │
│                     ┌──────────────┼──────────────┐     │
│                     │              │              │     │
│              ┌──────▼──┐   ┌──────▼──┐   ┌──────▼──┐   │
│              │AutoScout│   │Leboncoin│   │LaCentrale│  │
│              │  24.fr  │   │   .fr   │   │   .fr   │   │
│              └─────────┘   └─────────┘   └─────────┘   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    FILTER ENGINE                         │
│                                                         │
│  • Fuel: Essence / Hybride only                         │
│  • Year: Dynamic range (2023+ with 2-month lead)        │
│  • Condition: Non-accidenté                             │
│  • Price: User-defined max (EUR HT)                     │
│  • Export: Ready for international transfer             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Telegram Bot Token (via [@BotFather](https://t.me/BotFather))

### Installation

```bash
git clone https://github.com/dountiloua/CARDZSCRAP.git
cd CARDZSCRAP
pip install -r requirements.txt
```

### Configuration

```bash
export TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Run

```bash
python3 bot.py
```

### Deploy on Railway (24/7)

1. Push to GitHub
2. Connect repo on [railway.app](https://railway.app)
3. Add environment variable: `TELEGRAM_BOT_TOKEN`
4. Deploy — runs continuously

---

## 💬 Usage

### Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize and display welcome message |
| Enter price | Send any number (e.g., `10000`) to search |

### Search Flow

```
User: /start
Bot:  🚗 AUTO CAR SOURCER DZ
      Enter your maximum budget (EUR):

User: 10000
Bot:  🔍 Searching for vehicles under 10,000€...
      ⛽ Essence/Hybride | 📅 2023+ | 🛡️ Non-accidenté

      📌 AutoScout24.fr:
      🔗 [Click to view results](https://www.autoscout24.fr/...)

      📌 Leboncoin.fr:
      🔗 [Click to view results](https://www.leboncoin.fr/...)

      📌 LaCentrale.fr:
      🔗 [Click to view results](https://www.lacentrale.fr/...)
```

---

## 🌐 Supported Platforms

| Platform | Type | Coverage |
|----------|------|----------|
| AutoScout24.fr | Professional & Private | All France + cross-border |
| Leboncoin.fr | Private Listings | France nationwide |
| LaCentrale.fr | Certified Dealers | Premium listings |

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Bot Framework:** python-telegram-bot v20+
- **Search Method:** URL construction with encoded filter parameters (no scraping = no blocking)
- **Deployment:** Railway.app / Docker / Any VPS
- **Architecture:** Stateless agent — instant response, no database required

---

## 📋 Filter Specifications

| Parameter | Value |
|-----------|-------|
| Fuel Type | Essence (Gasoline) + Hybride |
| Min Year | Dynamic: Current Year - 3 + 2 months lead |
| Condition | Non-accidenté (no accident history) |
| Max Price | User-defined (EUR) |
| Excluded | Diesel, Full Electric, Damaged vehicles |

---

## 📈 Roadmap

- [x] Multi-platform URL generation
- [x] Smart filter engine
- [x] Telegram bot interface
- [x] Railway deployment
- [ ] Price tracking & alerts
- [ ] Specific model search (e.g., "Renault Arkana 1.3 TCe")
- [ ] PDF report generation
- [ ] Slack / Discord adapters
- [ ] REST API endpoint
- [ ] Dealer contact extraction

---

## 📄 License

MIT License — Free to use and modify.

---

<p align="center">
  <strong>Built by <a href="https://github.com/dountiloua">@dountiloua</a></strong><br>
  <em>Automating vehicle sourcing for the French export market</em>
</p>
