# Macro Signal Monitor

A lightweight macro monitoring tool built using FRED data and AI-assisted coding, designed for tracking key economic signals for decision support.

---

## Why it matters

**Macro Signal Monitor** is a lightweight dashboard I built using FRED data to track a curated set of macroeconomic indicators.

I developed it as a rapid prototype using AI-assisted coding tools to turn a loosely defined monitoring need into a usable internal tool.

The project demonstrates my ability to structure signals, integrate external data, and quickly build decision-oriented workflows.

This project matters not because it is a sophisticated macro investment tool, but because it demonstrates a shift in how I work:

- **From thinking → building**
  I had long wanted a simple way to monitor a curated set of macroeconomic indicators. This project is the first time I translated that idea into a working product.

- **From passive consumption → structured signal tracking**
  Instead of browsing scattered sources (FRED, articles, dashboards), I defined a small set of indicators that I believe are worth consistently tracking, and organized them into a single, low-friction interface.

- **From no-code → AI-assisted coding**
  I built this in one afternoon using AI coding tools. The goal was not perfection, but to learn how to turn a real-world monitoring need into a functional data product quickly.

- **Early proof of "builder" capability**
  This project is a concrete example that I can integrate external APIs, structure data into meaningful categories, design a usable interface for scanning information, and ship a working tool end-to-end.

> In short, this is about **developing the ability to productize ideas into usable systems.**

---

## What it does

- Fetches live data directly from the FRED API (cached hourly)
- Groups 24 indicators into 5 macro themes for structured scanning
- Shows headline metrics (10 key indicators) at a glance with period-over-period deltas
- Displays interactive time-series charts with per-chart definitions and recession shading
- Supports quick date presets (1Y, 5Y, 10Y, all) and custom date ranges
- Exports the currently selected data as CSV

---

## Indicators tracked

### 1. Monetary Policy & Rates
| Indicator | FRED ID | Notes |
|---|---|---|
| Federal Funds Rate | `FEDFUNDS` | The Fed's primary policy rate |
| Real Interest Rate (10Y) | `REAINTRATREARAT10Y` | Nominal yield minus inflation expectations |
| 10Y–2Y Treasury Spread | `T10Y2Y` | Most-watched yield curve inversion signal |
| 10Y–3M Treasury Spread | `T10Y3MM` | Academically preferred recession predictor |
| M2 Money Supply | `M2SL` | Broad money supply |
| Fed Balance Sheet | `WALCL` | Total Fed assets; expands in QE, shrinks in QT |

### 2. Growth & Inflation
| Indicator | FRED ID | Notes |
|---|---|---|
| Gross Domestic Product | `GDP` | Shown as YoY growth rate |
| Core PCE Price Index | `PCEPILFE` | **Fed's actual 2% inflation target**; shown as YoY |
| Core CPI (ex Food & Energy) | `CPILFENS` | Public headline inflation measure; shown as YoY |
| 10Y Breakeven Inflation Rate | `T10YIE` | Market-implied inflation expectations |
| Capacity Utilization: Manufacturing | `MCUMFN` | Upstream demand and inflation pressure indicator |

### 3. Labor Market
| Indicator | FRED ID | Notes |
|---|---|---|
| Unemployment Rate | `UNRATE` | Primary labor market slack measure |
| Nonfarm Payrolls | `PAYEMS` | Most-watched monthly jobs release |
| JOLTS Job Openings | `JTSJOL` | Labor demand; closely monitored by the Fed |
| Wages (Median Weekly Earnings) | `LES1252881600Q` | Real compensation and consumer purchasing power |
| Labor Share — Nonfarm Business | `PRS85006171` | Whether workers capture productivity gains |
| Indeed Job Postings: Software Dev | `IHLIDXUSTPSOFTDEVE` | Real-time tech sector hiring demand |

### 4. Markets & Financial Risk
| Indicator | FRED ID | Notes |
|---|---|---|
| S&P 500 | `SP500` | Broad U.S. equity benchmark |
| VIX (Market Volatility) | `VIXCLS` | Market "fear gauge" |
| High Yield Credit Spread | `BAMLH0A0HYM2` | Junk bond premium; spikes in credit stress |
| Baa Corporate Spread | `BAA10Y` | Investment-grade credit risk |
| St. Louis Financial Stress Index | `STLFSI4` | Composite financial market stress indicator |

### 5. Business & Housing
| Indicator | FRED ID | Notes |
|---|---|---|
| Corporate Profits After Tax | `A466RD3Q052SBEA` | Economy-wide profit health; billions of dollars SAAR |
| New Housing Units Authorized | `PERMIT` | Leading indicator of residential construction |

---

## Tech stack

| Layer | Tools |
|---|---|
| Language | Python 3.8+ |
| App framework | Streamlit |
| Charts | Plotly |
| Data | `fredapi`, Pandas |
| Secrets | `python-dotenv` (local), Streamlit secrets (cloud) |

---

## Setup

### Prerequisites
- Python 3.8+
- A free FRED API key — get one at [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)

### Run locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/fred-data-dashboard.git
cd fred-data-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and add your key: FRED_API_KEY=your_key_here

# 4. Launch
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → connect your repo → set `app.py` as the entry point
3. Under **Advanced settings → Secrets**, add:
```toml
FRED_API_KEY = "your_key_here"
```
4. Deploy — the app will be live at `your-app.streamlit.app`

---

## Limitations

- Lightweight monitoring tool, not a full investment decision engine
- Indicator interpretation is left to the user
- No alerting, AI-generated summaries, or decision journal layer yet

---

## Data source

All data is sourced from the [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org) database, maintained by the Federal Reserve Bank of St. Louis.
