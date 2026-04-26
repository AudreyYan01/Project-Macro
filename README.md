# Project Macro

A lightweight macroeconomic signals dashboard that turns public FRED data into a structured monitoring interface across inflation, labor, interest rates, markets, and business conditions.

**Live demo:** https://project-macro-nzju7gsrgshf77sfxn8f5u.streamlit.app/

---

## Why I Built This

Macroeconomic data is abundant but fragmented. FRED provides rich public data, but monitoring a focused set of indicators still requires switching across pages, charts, releases, and commentary.

I built Project Macro to turn a curated set of indicators into a repeatable review workflow. The goal was not to build a forecasting model or investment engine, but to practice converting an open-ended monitoring need into a usable data product.

This project demonstrates:

- External API integration

- Time-series data transformation

- Dashboard and information design

- Product framing for a loosely defined analytical workflow

- Rapid prototyping and deployment

---

## What It Does

Project Macro fetches live macroeconomic data from FRED and organizes it into a dashboard designed for quick, repeatable signal scanning.

Key features include:

- Fetches live data directly from the FRED API, with caching for faster reloads

- Groups 24 indicators into 5 macro themes for structured scanning

- Shows headline metrics for key indicators with latest value and period-over-period deltas

- Displays interactive time-series charts with per-chart definitions

- Supports time-window selection and custom date ranges

- Includes YoY calculations where useful

- Adds recession shading for historical context

- Allows CSV export of selected data

---

## Dashboard Themes

The dashboard organizes indicators into five macro themes:

1. **Inflation**  

   Tracks price pressure and inflation trends.

2. **Labor Market**  

   Tracks employment, unemployment, wage, and labor-force indicators.

3. **Interest Rates**  

   Tracks monetary-policy and yield-curve related indicators.

4. **Markets & Financial Conditions**  

   Tracks market stress, financial conditions, and risk signals.

5. **Business Conditions**  

   Tracks broader economic activity and business-cycle indicators.

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
git clone https://github.com/AudreyYan01/Project-Macro.git
cd Project-Macro

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
