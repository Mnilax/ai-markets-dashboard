# AI Model-Release Market Dashboard

Streamlit dashboard aggregating prediction markets about AI: model releases, regulation, capability milestones, and corporate events. Ships with a snapshot for instant demo.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

> ⚠️ **Data may be delayed. Not financial/trading advice.**

![Dashboard](assets/dashboard.svg)

## Features

- **4 categories** — Model releases, Regulation, Capability, Corporate
- **Market cards** — question, P(YES), volume, resolve date, source link
- **Filters & sorting** — by category, probability, volume, or close date
- **Offline demo** — `data/snapshot.json` committed for demo without API keys

## Install

```bash
pip install -e .
```

## Quickstart

```bash
# Run with bundled snapshot (no API keys needed)
streamlit run app.py
```

The dashboard opens at `http://localhost:8501` with data from `data/snapshot.json`.

### Live mode (optional)

```bash
cp .env.example .env
# Add your Kalshi / Polymarket API keys to .env
streamlit run app.py
```

With API keys configured, the dashboard fetches live market data on each refresh.

## How It Works

1. **Fetch** — pulls active markets from Kalshi REST API and Polymarket CLOB API via `httpx`
2. **Curate** — categorizes markets by keyword rules (model release, regulation, capability, corporate)
3. **Display** — Streamlit renders filterable, sortable market cards with probability highlights

Without API keys, the app loads `data/snapshot.json` — a pre-fetched dataset committed to the repo so the dashboard is always demoable.

## Architecture

```
app.py                     # Streamlit entry point
data/snapshot.json         # Pre-fetched market snapshot for offline demo
src/aimarkets/
├── fetch.py               # Kalshi + Polymarket API clients
├── curate.py              # Category classification + sorting
└── models.py              # Market data models
```

## Roadmap

- [ ] Auto-refresh with configurable interval
- [ ] Historical price charts per market
- [ ] Alerts for large probability moves
- [ ] Additional sources (Metaculus, Manifold)

## License

MIT
