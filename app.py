"""
FRED Economic Dashboard
Real-time economic data visualization using FRED API
"""

import math
import textwrap
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
from dotenv import load_dotenv

load_dotenv('.env')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from fred_api import FREDDataFetcher

# 10 headline indicators shown in the key metrics row (only those also selected in sidebar)
HEADLINE_SERIES = [
    'FEDFUNDS',       # monetary policy anchor
    'PCEPILFE',       # Fed's actual inflation target (Core PCE)
    'CPILFENS',       # Core CPI — public headline inflation
    'UNRATE',         # unemployment
    'PAYEMS',         # nonfarm payrolls — most-watched monthly release
    'GDP',            # output growth
    'T10Y2Y',         # yield curve — mainstream recession signal
    'SP500',          # equities
    'BAMLH0A0HYM2',   # credit stress
    'WALCL',          # Fed balance sheet / QE-QT
]

st.set_page_config(
    page_title="FRED Economic Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_fred_client(api_key):
    try:
        return FREDDataFetcher(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing FRED API: {str(e)}")
        return None


@st.cache_data(ttl=3600)
def fetch_data(_fred_client, series_ids, start_date, end_date):
    return _fred_client.fetch_multiple_series(list(series_ids), start_date, end_date)


def create_individual_chart(df, series_id, fred_client, show_recessions=True, display_start=None, display_end=None):
    if df.empty or series_id not in df.columns:
        return None

    series_data = df[series_id].dropna()
    if series_data.empty:
        return None

    info = fred_client.get_series_info(series_id)

    if info.get('show_yoy', False):
        frequency = info.get('frequency', 'Monthly')
        if frequency == 'Quarterly':
            shift_periods = 4
        elif frequency == 'Annual':
            shift_periods = 1
        else:
            shift_periods = 12

        yoy_growth = ((series_data - series_data.shift(shift_periods)) / series_data.shift(shift_periods)) * 100
        plot_data = yoy_growth.dropna()
        y_label = 'YoY Growth Rate (%)'
        chart_title = f"{info['name']} — YoY Growth Rate"
    else:
        plot_data = series_data
        y_label = info['units']
        chart_title = info['name']

    if display_start is not None and display_end is not None:
        plot_data = plot_data[display_start:display_end]

    if plot_data.empty:
        return None

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=plot_data.index,
            y=plot_data.values,
            name=chart_title,
            line=dict(color='#1f77b4', width=2),
            mode='lines',
            hovertemplate='%{x|%Y-%m-%d}: %{y:.2f}<extra></extra>'
        )
    )

    if show_recessions:
        for rec_start, rec_end in FREDDataFetcher.RECESSION_PERIODS:
            rec_start_dt = pd.to_datetime(rec_start)
            rec_end_dt = pd.to_datetime(rec_end)
            if rec_start_dt <= plot_data.index.max() and rec_end_dt >= plot_data.index.min():
                fig.add_vrect(
                    x0=rec_start_dt, x1=rec_end_dt,
                    fillcolor="gray", opacity=0.2, layer="below", line_width=0,
                )

    # Y-axis: start from 0 for non-negative data, from floor integer when data goes negative
    y_min = plot_data.min()
    if y_min >= 0:
        y_axis = dict(rangemode='tozero')
    else:
        y_axis = dict(range=[math.floor(y_min), None])

    # Build title with description subtitle embedded in the chart
    description = info.get('description', '')
    if description:
        wrapped = '<br>'.join(textwrap.wrap(description, width=90))
        title_html = f"<b>{chart_title}</b><br><sup style='color:#555555'>{wrapped}</sup>"
        top_margin = 100
    else:
        title_html = f"<b>{chart_title}</b>"
        top_margin = 55

    fig.update_layout(
        title=dict(text=title_html, font=dict(size=14)),
        xaxis_title="Date",
        yaxis=dict(title=y_label, **y_axis),
        hovermode='x unified',
        height=420,
        showlegend=False,
        margin=dict(l=50, r=20, t=top_margin, b=50)
    )

    return fig


_CHART_CONFIG = {
    'modeBarButtonsToKeep': ['toImage'],
    'displaylogo': False,
}


def render_chart_panel(fig, series_id, info, start_date_str, end_date_str):
    st.plotly_chart(fig, use_container_width=True, config=_CHART_CONFIG)
    source_url = info.get('url', f'https://fred.stlouisfed.org/series/{series_id}')
    unit_label = "YoY Growth Rate (%)" if info.get('show_yoy', False) else info.get('units', 'Unknown')
    st.caption(
        f"**{info['name']}** ({series_id}) · {start_date_str} to {end_date_str} · "
        f"Unit: {unit_label} · Source: FRED · [View on FRED →]({source_url})"
    )


def main():
    st.markdown('<p class="main-header">📊 FRED Economic Data Dashboard</p>', unsafe_allow_html=True)
    st.caption(
        "A focused macro signal monitor for tracking inflation, rates, growth, labor, credit, "
        "markets, and financial conditions from FRED."
    )

    categories = {
        # The Fed's policy tools and their transmission into the economy
        "Monetary Policy & Rates": [
            'FEDFUNDS', 'REAINTRATREARAT10Y', 'T10Y2Y', 'T10Y3MM', 'M2SL', 'WALCL',
        ],
        # Output, price level, and inflation expectations
        "Growth & Inflation": [
            'GDP', 'PCEPILFE', 'CPILFENS', 'T10YIE', 'MCUMFN',
        ],
        # Jobs, wages, and labor market capacity
        "Labor Market": [
            'UNRATE', 'PAYEMS', 'JTSJOL', 'LES1252881600Q', 'PRS85006171',
            'IHLIDXUSTPSOFTDEVE',
        ],
        # Market-based measures of risk appetite and financial stress
        "Markets & Financial Risk": [
            'SP500', 'VIXCLS', 'BAMLH0A0HYM2', 'BAA10Y', 'STLFSI4',
        ],
        # Corporate health and real-economy investment
        "Business & Housing": [
            'A466RD3Q052SBEA', 'PERMIT',
        ],
    }

    with st.sidebar:
        st.header("⚙️ Configuration")

        # API key priority: st.secrets → .env → sidebar input
        # Only read st.secrets if a secrets file actually exists — calling it without
        # a file causes Streamlit to render an error box even inside a try/except.
        _secrets_paths = [
            os.path.expanduser("~/.streamlit/secrets.toml"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit", "secrets.toml"),
        ]
        api_key = None
        if any(os.path.exists(p) for p in _secrets_paths):
            try:
                api_key = st.secrets.get("FRED_API_KEY", None)
            except Exception:
                pass
        api_key = api_key or os.getenv('FRED_API_KEY')

        if not api_key:
            api_key = st.text_input(
                "FRED API Key",
                type="password",
                help="Enter your FRED API key. Get one free at https://fred.stlouisfed.org/docs/api/api_key.html"
            )
            if not api_key:
                st.warning("⚠️ Please enter your FRED API key to continue")
                st.info(
                    "**How to get a FRED API key:**\n\n"
                    "1. Go to https://fred.stlouisfed.org\n"
                    "2. Create a free account or log in\n"
                    "3. Request an API key at the FRED API docs page\n"
                    "4. Copy and paste your API key above"
                )
                st.stop()

        fred_client = get_fred_client(api_key)
        if fred_client is None:
            st.stop()

        st.success("✅ Connected to FRED API")
        st.markdown("---")

        # Date range selection
        st.header("📅 Date Range")
        date_preset = st.selectbox(
            "Quick Select",
            ["Last 3 Months", "Last 6 Months", "Last 1 Year", "Last 5 Years",
             "Last 10 Years", "Last 20 Years", "All Available", "Custom"],
            index=3  # default: Last 5 Years
        )

        today = datetime.now()

        if date_preset == "Last 3 Months":
            start_date = today - timedelta(days=90)
            end_date = today
        elif date_preset == "Last 6 Months":
            start_date = today - timedelta(days=180)
            end_date = today
        elif date_preset == "Last 1 Year":
            start_date = today - timedelta(days=365)
            end_date = today
        elif date_preset == "Last 5 Years":
            start_date = today - timedelta(days=365 * 5)
            end_date = today
        elif date_preset == "Last 10 Years":
            start_date = today - timedelta(days=365 * 10)
            end_date = today
        elif date_preset == "Last 20 Years":
            start_date = today - timedelta(days=365 * 20)
            end_date = today
        elif date_preset == "All Available":
            start_date = datetime(1950, 1, 1)
            end_date = today
        else:  # Custom
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=today - timedelta(days=365 * 5))
            with col2:
                end_date = st.date_input("End Date", value=today)

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Fetch extra data before display start for YoY calculations (~18 months)
        fetch_start_date = (start_date - timedelta(days=550)).strftime('%Y-%m-%d')
        fetch_end_date = end_date_str

        st.markdown("---")

        # Indicator selection
        st.header("📈 Indicators")
        selected_series = []
        for category, series_list in categories.items():
            with st.expander(category):
                for series_id in series_list:
                    info = fred_client.get_series_info(series_id)
                    if st.checkbox(info['name'], key=series_id, value=True):
                        selected_series.append(series_id)

        st.markdown("---")

        # Chart options
        st.header("🎨 Chart Options")
        show_recessions = st.checkbox("Show Recession Periods", value=True)

        # Auto-refresh
        st.markdown("---")
        st.header("🔄 Auto Refresh")
        auto_refresh = st.checkbox("Enable Auto Refresh")
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval (minutes)", 1, 60, 15)
            st.info(f"Dashboard will refresh every {refresh_interval} min.")
            try:
                from streamlit_autorefresh import st_autorefresh
                st_autorefresh(interval=refresh_interval * 60 * 1000, key="autorefresh")
            except ImportError:
                st.caption("Install `streamlit-autorefresh` to enable background refresh.")

    # Main content area
    if not selected_series:
        st.info("👈 Please select at least one economic indicator from the sidebar to begin")
        st.stop()

    with st.spinner("📥 Fetching data from FRED..."):
        df_full = fetch_data(fred_client, tuple(selected_series), fetch_start_date, fetch_end_date)

    if df_full.empty:
        st.error("❌ No data available for the selected indicators and date range")
        st.stop()

    df_display = df_full[start_date_str:end_date_str]
    last_observation = df_display.dropna(how="all").index.max() if not df_display.empty else None
    loaded_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    if last_observation is not None:
        st.info(
            f"Last updated: {loaded_at} · Latest data point: {last_observation.strftime('%Y-%m-%d')} · "
            "Source: Federal Reserve Economic Data (FRED), Federal Reserve Bank of St. Louis."
        )
    else:
        st.info(
            f"Last updated: {loaded_at} · "
            "Source: Federal Reserve Economic Data (FRED), Federal Reserve Bank of St. Louis."
        )

    # Headline metrics — up to 10 key indicators, only those selected in sidebar
    # Derived from df_full directly (no extra API calls)
    headline = [sid for sid in HEADLINE_SERIES if sid in selected_series and sid in df_full.columns]
    if headline:
        st.header("📊 Key Indicators")
        n_cols = 5  # two rows of 5 keeps columns readable
        for row_start in range(0, len(headline), n_cols):
            row_ids = headline[row_start:row_start + n_cols]
            metric_cols = st.columns(n_cols)
            for col, series_id in zip(metric_cols, row_ids):
                info = fred_client.get_series_info(series_id)
                series_data = df_full[series_id].dropna()
                with col:
                    if series_data.empty:
                        st.metric(label=info['name'], value="N/A")
                        continue
                    latest_value = series_data.iloc[-1]
                    latest_date = series_data.index[-1].strftime('%Y-%m-%d')
                    if len(series_data) >= 2:
                        prev_value = series_data.iloc[-2]
                        prev_date = series_data.index[-2].strftime('%Y-%m-%d')
                        change = latest_value - prev_value
                        units = info.get('units', '').lower()
                        if 'percent' in units or series_id in ['FEDFUNDS', 'T10Y3MM', 'REAINTRATREARAT10Y', 'UNRATE']:
                            delta_str = f"{change:+.2f} pp"
                        else:
                            pct_change = (change / prev_value) * 100 if prev_value != 0 else 0
                            delta_str = f"{pct_change:+.2f}%"
                        st.metric(
                            label=info['name'],
                            value=f"{latest_value:.2f}",
                            delta=delta_str,
                            help=f"As of {latest_date} (prev: {prev_date})"
                        )
                    else:
                        st.metric(label=info['name'], value=f"{latest_value:.2f}", help=f"As of {latest_date}")

    # Build all charts once; skip series with no data in the selected range
    st.header("📈 Time Series Charts")
    charts = {}
    for sid in selected_series:
        fig = create_individual_chart(df_full, sid, fred_client, show_recessions, start_date_str, end_date_str)
        if fig is not None:
            charts[sid] = fig

    if not charts:
        st.warning("No chart data available for the selected indicators and date range.")
    else:
        # Render charts grouped by category — each category starts a new row
        for category, series_list in categories.items():
            category_charts = [(sid, charts[sid]) for sid in series_list if sid in charts]
            if not category_charts:
                continue
            st.subheader(category)
            for i in range(0, len(category_charts), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(category_charts):
                        sid, fig = category_charts[i + j]
                        with col:
                            render_chart_panel(fig, sid, fred_client.get_series_info(sid), start_date_str, end_date_str)

    # Raw data table
    with st.expander("📋 View Raw Data"):
        st.dataframe(df_display, use_container_width=True)
        csv = df_display.to_csv()
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"fred_data_{start_date_str}_to_{end_date_str}.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Data Source: Federal Reserve Economic Data (FRED) · Federal Reserve Bank of St. Louis · Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
