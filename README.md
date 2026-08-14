<p align="center">
  <img src="https://img.shields.io/badge/🚗-DzCarPenny-red?style=for-the-badge&labelColor=1a1a2e" alt="DzCarPenny">
</p>

<h1 align="center">DzCarPenny</h1>

<p align="center">
  <strong>AI-Powered Automotive Price Tracking Agent for the French Used Car Market</strong><br>
  <em>Autonomous sourcing, real-time direct links, and 12h price monitoring — built for export</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/platforms-AutoScout24%20%7C%20Leboncoin%20%7C%20LaCentrale-blue?style=flat-square" alt="Platforms">
  <img src="https://img.shields.io/badge/monitoring-12h%20auto--track-orange?style=flat-square" alt="Monitoring">
  <img src="https://img.shields.io/badge/agent-autonomous-blueviolet?style=flat-square" alt="Agent">
  <img src="https://img.shields.io/badge/deploy-Cloud%20Agent%20Platform-purple?style=flat-square" alt="Deploy">
</p>

---

## 🎯 What Is DzCarPenny?

**DzCarPenny** is an autonomous AI agent that sources, tracks, and monitors used car prices across the French market. Unlike simple search tools, DzCarPenny operates as a **persistent intelligent agent** that:

- **Searches on demand** — enter a budget and get instant results with **direct clickable links** to each listing
- **Monitors every 12 hours** — automatically re-checks prices and alerts you when new deals appear or prices drop
- **Delivers results in Telegram** — each car comes with a direct URL to the listing, ready to click and contact the seller
- **Covers 3 major platforms** — AutoScout24.fr, Leboncoin.fr, LaCentrale.fr

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 Autonomous Agent | Runs 24/7, searches and monitors without manual intervention |
| 🔔 12h Price Tracking | Auto-checks every 12 hours — alerts on price drops, new listings, or confirms "no changes" |
| 🔗 Direct Car Links | Every result includes a **clickable URL** to the exact listing page |
| 🔍 Multi-Platform Search | Queries AutoScout24.fr, Leboncoin.fr, and LaCentrale.fr simultaneously |
| ⛽ Smart Fuel Filter | Gasoline & Hybrid only — no diesel, no full electric |
| 📅 Dynamic Date Logic | Auto-calculates valid year range (current year - 3 + 2 months lead) |
| 🛡️ Condition Filter | Strictly non-accidenté (no accident history) |
| 💰 User-Defined Budget | Set your max price in EUR (HT for export) |
| 📱 Telegram Delivery | Results delivered directly in Telegram with formatted cards |
| 📄 Report Generation | Sends organized summary report after each search |

---

## 📱 Telegram Output Format

Each car result is delivered with a **direct link** to the listing:

```
🚗 Citroën C3 1.2 PureTech Shine (2023)
💰 Price: 9,990€
⛽ Fuel: Essence
🛣️ Mileage: 24,403 km
📍 Location: Paris (75002)
🔗 Link: https://www.autoscout24.fr/offres/citroen-c3-...
🛠️ Status: Non-accidenté
📌 Source: AutoScout24
```

After all results, the agent sends a **summary report** with all listings organized.

---

## 🔔 12-Hour Autonomous Monitoring

Once you search, DzCarPenny activates its **monitoring daemon**:

```
⏰ Auto-check schedule: 08:00 & 20:00 daily

📉 Price dropped?  → Instant alert with new price + link
🆕 New listing?    → Sends full details immediately  
✅ No changes?     → "Same results, still €X cheapest"
```

You search once. The agent watches forever (until you stop it).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  DzCarPenny — AI AGENT                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌──────────────────────────────┐    │
│  │  Telegram   │    │      Agent Core              │    │
│  │  Adapter    │───►│  (Search + Monitor + Alert)  │    │
│  └─────────────┘    └──────────────┬───────────────┘    │
│                                    │                    │
│                     ┌──────────────┼──────────────┐     │
│                     │              │              │     │
│              ┌──────▼──┐   ┌──────▼──┐   ┌──────▼──┐   │
│              │AutoScout│   │Leboncoin│   │LaCentrale│  │
│              │  24.fr  │   │   .fr   │   │   .fr   │   │
│              └────┬────┘   └────┬────┘   └────┬────┘   │
│                   │             │             │         │
│              ┌────▼─────────────▼─────────────▼────┐    │
│              │        DIRECT LINK RESOLVER          │    │
│              │   (Extracts individual listing URLs) │    │
│              └─────────────────┬────────────────────┘    │
│                               │                         │
│              ┌────────────────▼────────────────────┐    │
│              │     12h MONITORING DAEMON            │    │
│              │  (Price diff + New listing detect)   │    │
│              └─────────────────────────────────────┘    │
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
git clone https://github.com/dountiloua/DzCarPenny.git
cd DzCarPenny
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env:
# TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Run

```bash
python3 bot.py
```

---

## ☁️ 24/7 Deployment

DzCarPenny is a **cloud-native autonomous agent** with configuration files (`Procfile`, `runtime.txt`) for deployment on any agent hosting platform:

1. Push repository to your Git provider.
2. Connect to your cloud agent platform.
3. Set environment variable: `TELEGRAM_BOT_TOKEN`
4. Deploy — the agent runs continuously, handling searches and executing the 12h monitoring daemon.

**Compatible with:** Any container-based PaaS, serverless workers, VPS, Docker, or dedicated agent infrastructure.

---

## 💬 Usage

### Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize agent and display welcome |
| Enter price | Send any number (e.g., `10000`) to search |
| `/monitor` | View active price tracking status |
| `/stop` | Stop monitoring |

### Flow

```
User: /start
Agent: 🚗 DzCarPenny — AI Car Sourcing Agent
       Enter your maximum budget (EUR):

User: 10000
Agent: 🔍 Searching 3 platforms...
       ⛽ Essence/Hybride | 📅 2023+ | 🛡️ Non-accidenté

       [Individual car results with direct links]

       🔔 MONITORING ACTIVATED
       ⏰ Next check in 12h (08:00 & 20:00)
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Agent Framework:** python-telegram-bot v20+ with APScheduler
- **Search Method:** Multi-platform URL construction + link resolution
- **Monitoring:** Cron-based 12h daemon with price diff detection
- **Deployment:** Cloud-native, container-ready (`Procfile`, `runtime.txt`)

---

## 📋 Filter Specifications

| Parameter | Value |
|-----------|-------|
| Fuel Type | Essence (Gasoline) + Hybride |
| Min Year | Dynamic: Current Year - 3 + 2 months lead |
| Condition | Non-accidenté (no accident history) |
| Max Price | User-defined (EUR HT) |
| Excluded | Diesel, Full Electric, Damaged vehicles |
| Links | Direct URL to each individual listing |

---

## 📈 Roadmap

- [x] Multi-platform search (AutoScout24, Leboncoin, LaCentrale)
- [x] Direct links to individual listings
- [x] 12h autonomous price monitoring
- [x] Price drop / new listing alerts
- [x] Telegram delivery with formatted cards
- [x] Summary report generation
- [ ] Specific model search (e.g., "Renault Arkana 1.3 TCe")
- [ ] Photo thumbnails in results
- [ ] Price history charts
- [ ] Slack / Discord adapters
- [ ] REST API endpoint

---

## 📄 License

MIT License — Free to use and modify.

---

<p align="center">
  <strong>Built by <a href="https://github.com/dountiloua">@dountiloua</a></strong><br>
  <em>Autonomous vehicle sourcing for the French export market</em>
</p>
