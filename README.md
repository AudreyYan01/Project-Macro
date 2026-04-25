**Happy Analyzing!** 📊📈

# Macro Signal Monitor

A lightweight macro monitoring dashboard built with Python, Streamlit, and FRED data.

I built this project in one afternoon primarily to learn AI-assisted coding by turning a real monitoring need into a usable internal tool. It tracks a curated set of macroeconomic indicators I wanted to follow in one place and serves as an early prototype of a decision-support workflow rather than a full investment product.

## Why this project matters

This project matters less as a polished market tool and more as evidence of how I work:

- **From thinking to building:** I translated an idea I had been carrying for a while into a working product.
- **AI-assisted rapid prototyping:** I used AI coding tools to accelerate implementation and learn by shipping.
- **Signal organization:** I selected and grouped indicators into a lower-friction monitoring workflow instead of relying on scattered sources.
- **Builder proof point:** The project shows that I can integrate external APIs, structure data into usable categories, and create a functional interface end-to-end.

## What it does

The dashboard helps users monitor a selected set of macroeconomic indicators from FRED in one place.

Core capabilities include:

- Fetching recent data directly from the FRED API
- Grouping indicators by macro theme
- Supporting quick date presets and custom date ranges
- Displaying latest values and recent changes
- Visualizing multiple indicators interactively
- Highlighting recession periods for historical context
- Exporting the currently selected data as CSV

## Indicators tracked

### Inflation & Prices
- Core CPI (excluding Food & Energy)

### Interest Rates
- Federal Funds Rate
- 10Y-3M Treasury Spread
- Real Interest Rate (10Y)

### Economic Output
- Gross Domestic Product (GDP)
- Capacity Utilization: Manufacturing

### Labor Market
- Unemployment Rate
- Labor Share of GDP
- Nonfarm Business Labor Share
- Wages

### Housing
- New Housing Units Authorized (Building Permits)

### Financial Markets
- S&P 500
- VIX (Market Volatility Index)

### Credit & Spreads
- High Yield Credit Spread
- Baa Corporate Bond Spread

### Corporate Performance
- Corporate Profits After Tax

### Financial Conditions
- St Louis Financial Stress Index
- Nonfinancial Leverage Index

### Monetary Indicators
- M2 Money Supply
- Federal Reserve Balance Sheet

## Why I chose these indicators

I chose these indicators because they are useful for regularly scanning broad macro conditions across inflation, rates, growth, labor, credit, and financial conditions. The goal was not to build a complete macro model, but to create a practical monitoring set that reduces friction in keeping track of signals that matter.

## Tech stack

- Python
- Streamlit
- Plotly
- Pandas
- `fredapi`

## Project structure

```text
FRED Data Dashboard/
├── app.py                      # Main Streamlit dashboard application
├── src/
│   └── fred_api.py            # FRED API interaction module
├── data/                       # Downloaded data cache (auto-generated)
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment file
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Setup

### Prerequisites
- Python 3.8 or higher
- FRED API key

### Step 1: Get a FRED API Key

1. Go to [https://fred.stlouisfed.org](https://fred.stlouisfed.org)
2. Create a free account or log in
3. Request an API key at [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
4. Your API key will be emailed to you

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

Or use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

## Example workflow

A typical use case is:

1. Select a time range
2. Choose indicators across themes such as inflation, labor, rates, and credit
3. Scan recent values and directional changes
4. Compare chart behavior across time periods and recession windows
5. Export the data if deeper analysis is needed elsewhere

## What I learned

- AI coding tools are useful for quickly moving from concept to prototype
- A small internal tool becomes more valuable when the signal set is intentionally curated
- Even a lightweight dashboard benefits from clearer framing around the decision workflow it supports
- Building something functional quickly is a good way to surface what should be improved in a second version

## Limitations

- This is a lightweight monitoring tool, not a full investment decision engine
- Indicator interpretation is still left to the user
- There is no alerting, summarization, or decision journal layer yet
- The current version prioritizes usability and speed over deeper analytical functionality

## Potential next steps

- Add indicator notes explaining why each signal matters
- Add rule-based summaries or simple regime labels
- Improve modularization of the data and UI layers
- Add a lightweight decision journal or watchlist feature
- Optionally add AI-generated summaries in a future version

## Data source

All data comes from the Federal Reserve Economic Data (FRED) database maintained by the Federal Reserve Bank of St. Louis.

- FRED Website: [https://fred.stlouisfed.org](https://fred.stlouisfed.org)
- FRED API Documentation: [https://fred.stlouisfed.org/docs/api/](https://fred.stlouisfed.org/docs/api/)

## Credits

Built with:
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [fredapi](https://github.com/mortada/fredapi)
- [Pandas](https://pandas.pydata.org/)

Data provided by Federal Reserve Economic Data (FRED), Federal Reserve Bank of St. Louis.