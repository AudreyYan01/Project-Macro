"""
FRED API Data Fetcher Module
Handles all interactions with the Federal Reserve Economic Data (FRED) API
"""

import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional


class FREDDataFetcher:
    """Class to handle FRED API data fetching and processing"""

    # Economic indicators configuration based on your data dictionary
    INDICATORS = {
        'CPILFENS': {
            'name': 'Core CPI (ex Food & Energy)',
            'units': 'Index 1982-1984=100',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/CPILFENS',
            'show_yoy': True,
            'description': (
                "Tracks price changes for consumer goods and services excluding volatile food and energy — "
                "the Fed's preferred gauge of underlying inflation."
            ),
        },
        'FEDFUNDS': {
            'name': 'Federal Funds Rate',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/FEDFUNDS',
            'description': (
                "The overnight rate at which banks lend reserves to each other, set by the Federal Reserve "
                "as the primary lever for controlling inflation and stimulating or cooling the economy."
            ),
        },
        'GDP': {
            'name': 'Gross Domestic Product',
            'units': 'Billions of Dollars',
            'seasonal_adj': True,
            'frequency': 'Quarterly',
            'url': 'https://fred.stlouisfed.org/series/GDP',
            'show_yoy': True,
            'description': (
                "The total market value of all goods and services produced in the U.S. — "
                "the broadest single measure of economic output and health."
            ),
        },
        'MCUMFN': {
            'name': 'Capacity Utilization: Manufacturing',
            'units': 'Percent of Capacity',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/MCUMFN',
            'description': (
                "The share of manufacturing capacity currently in use; readings above 80% can signal "
                "inflationary pressure, while sharp drops indicate industrial contraction."
            ),
        },
        'T10Y3MM': {
            'name': '10Y-3M Treasury Spread',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/T10Y3MM',
            'description': (
                "The gap between 10-year and 3-month Treasury yields; sustained inversion (negative values) "
                "has preceded every U.S. recession over the past 50 years."
            ),
        },
        'PERMIT': {
            'name': 'New Housing Units Authorized',
            'units': 'Thousands of Units',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/PERMIT',
            'description': (
                "The count of new residential building permits issued monthly — a leading indicator of "
                "construction activity and household formation demand."
            ),
        },
        'SP500': {
            'name': 'S&P 500',
            'units': 'Index',
            'seasonal_adj': False,
            'frequency': 'Daily',
            'url': 'https://fred.stlouisfed.org/series/SP500',
            'description': (
                "A market-cap-weighted index of 500 large U.S. companies, widely used as the benchmark "
                "for U.S. equity performance and as a forward-looking indicator of economic sentiment."
            ),
        },
        'BAMLH0A0HYM2': {
            'name': 'High Yield Credit Spread',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Daily',
            'url': 'https://fred.stlouisfed.org/series/BAMLH0A0HYM2',
            'description': (
                "The yield premium that junk-rated bonds carry over Treasuries; spikes signal rising "
                "credit stress and risk aversion in financial markets."
            ),
        },
        'BAA10Y': {
            'name': 'Baa Corporate Spread',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Daily',
            'url': 'https://fred.stlouisfed.org/series/BAA10Y',
            'description': (
                "The yield difference between Baa-rated (lowest investment-grade) corporate bonds and "
                "10-year Treasuries, measuring perceived credit risk in the broader corporate sector."
            ),
        },
        'A466RD3Q052SBEA': {
            'name': 'Corporate Profits After Tax',
            'units': 'Billions of Dollars, SAAR',
            'seasonal_adj': True,
            'frequency': 'Quarterly',
            'url': 'https://fred.stlouisfed.org/series/A466RD3Q052SBEA',
            'description': (
                "After-tax profits earned by U.S. corporations, adjusted for inventory valuation and "
                "capital consumption — a key driver of business investment and hiring decisions."
            ),
        },
        'LES1252881600Q': {
            'name': 'Wages (Median Weekly Earnings)',
            'units': 'Dollars',
            'seasonal_adj': True,
            'frequency': 'Quarterly',
            'url': 'https://fred.stlouisfed.org/series/LES1252881600Q',
            'description': (
                "Median usual weekly earnings of full-time wage and salary workers, reflecting real "
                "labor compensation and consumer purchasing power."
            ),
        },
        'VIXCLS': {
            'name': 'VIX (Market Volatility)',
            'units': 'Index',
            'seasonal_adj': False,
            'frequency': 'Daily',
            'url': 'https://fred.stlouisfed.org/series/VIXCLS',
            'description': (
                "The CBOE Volatility Index measures expected 30-day S&P 500 volatility implied by options "
                "prices — commonly called the market's \"fear gauge.\""
            ),
        },
        'NFCINONFINLEVERAGE': {
            'name': 'Nonfinancial Leverage Index',
            'units': 'Index',
            'seasonal_adj': False,
            'frequency': 'Weekly',
            'url': 'https://fred.stlouisfed.org/series/NFCINONFINLEVERAGE',
            'description': (
                "Measures leverage conditions in nonfinancial sectors; rising values indicate that "
                "households and businesses are increasingly reliant on borrowed funds."
            ),
        },
        'STLFSI4': {
            'name': 'St. Louis Financial Stress Index',
            'units': 'Index',
            'seasonal_adj': False,
            'frequency': 'Weekly',
            'url': 'https://fred.stlouisfed.org/series/STLFSI4',
            'description': (
                "A composite of 18 financial market variables; values above zero signal above-average "
                "stress in U.S. financial markets, while negative values indicate calm conditions."
            ),
        },
        'LABSHPUSA156NRUG': {
            'name': 'Labor Share of GDP',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Annual',
            'url': 'https://fred.stlouisfed.org/series/LABSHPUSA156NRUG',
            'description': (
                "The share of national income paid to workers as compensation; a declining trend "
                "signals that productivity gains are accruing to capital rather than labor."
            ),
        },
        'PRS85006171': {
            'name': 'Labor Share — Nonfarm Business',
            'units': 'Percent',
            'seasonal_adj': True,
            'frequency': 'Quarterly',
            'url': 'https://fred.stlouisfed.org/series/PRS85006171',
            'description': (
                "Labor compensation as a share of nonfarm business output, tracking whether workers "
                "capture a proportional share of productivity improvements each quarter."
            ),
        },
        'UNRATE': {
            'name': 'Unemployment Rate',
            'units': 'Percent',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/UNRATE',
            'description': (
                "The percentage of the labor force that is jobless and actively seeking work — "
                "the headline measure of labor market slack and a key Fed dual-mandate target."
            ),
        },
        'REAINTRATREARAT10Y': {
            'name': 'Real Interest Rate (10Y)',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/REAINTRATREARAT10Y',
            'description': (
                "The 10-year Treasury yield adjusted for inflation expectations, reflecting the true "
                "long-term cost of borrowing and the stance of monetary policy in real terms."
            ),
        },
        'M2SL': {
            'name': 'M2 Money Supply',
            'units': 'Billions of Dollars',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/M2SL',
            'description': (
                "Broad money supply including cash, checking deposits, and savings accounts; "
                "rapid M2 growth can foreshadow inflation, while contraction may signal tighter conditions."
            ),
        },
        'WALCL': {
            'name': 'Fed Balance Sheet (Total Assets)',
            'units': 'Millions of Dollars',
            'seasonal_adj': False,
            'frequency': 'Weekly',
            'url': 'https://fred.stlouisfed.org/series/WALCL',
            'description': (
                "Total assets held by the Federal Reserve; expansion signals quantitative easing (QE) "
                "injecting liquidity, while shrinkage signals quantitative tightening (QT)."
            ),
        },
        'IHLIDXUSTPSOFTDEVE': {
            'name': 'Indeed Job Postings: Software Development (US)',
            'units': 'Index (Feb 1, 2020 = 100)',
            'seasonal_adj': True,
            'frequency': 'Daily',
            'url': 'https://fred.stlouisfed.org/series/IHLIDXUSTPSOFTDEVE',
            'description': (
                "7-day moving average of U.S. software development job postings on Indeed, "
                "indexed to a pre-pandemic baseline — a leading indicator of tech sector hiring demand."
            ),
        },
        'PCEPILFE': {
            'name': 'Core PCE Price Index',
            'units': 'Index (2017=100)',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/PCEPILFE',
            'show_yoy': True,
            'description': (
                "The Fed's preferred inflation gauge, measuring personal consumption expenditure prices "
                "excluding food and energy; the FOMC's 2% inflation target is defined in terms of this index."
            ),
        },
        'PAYEMS': {
            'name': 'Nonfarm Payrolls',
            'units': 'Thousands of Persons',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/PAYEMS',
            'description': (
                "Total paid workers across all non-farm industries; the most closely watched monthly "
                "economic release, with month-over-month changes signaling labor market strength or weakness."
            ),
        },
        'T10YIE': {
            'name': '10-Year Breakeven Inflation Rate',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Daily',
            'url': 'https://fred.stlouisfed.org/series/T10YIE',
            'description': (
                "Market-implied average inflation over the next 10 years, derived from the yield gap "
                "between nominal and inflation-protected Treasuries (TIPS); a rise signals de-anchoring inflation expectations."
            ),
        },
        'T10Y2Y': {
            'name': '10Y-2Y Treasury Spread',
            'units': 'Percent',
            'seasonal_adj': False,
            'frequency': 'Daily',
            'url': 'https://fred.stlouisfed.org/series/T10Y2Y',
            'description': (
                "The yield gap between 10-year and 2-year Treasuries — the most widely cited yield curve "
                "measure; sustained inversion (below zero) has preceded every U.S. recession in modern history."
            ),
        },
        'JTSJOL': {
            'name': 'JOLTS Job Openings',
            'units': 'Thousands of Jobs',
            'seasonal_adj': True,
            'frequency': 'Monthly',
            'url': 'https://fred.stlouisfed.org/series/JTSJOL',
            'description': (
                "The number of unfilled job positions across the U.S. economy; a high openings-to-unemployed "
                "ratio signals a tight labor market and upward wage pressure — closely monitored by the Fed."
            ),
        },
    }

    # NBER Recession periods for shading
    RECESSION_PERIODS = [
        ('1957-08-01', '1958-04-01'),
        ('1960-04-01', '1961-02-01'),
        ('1969-12-01', '1970-11-01'),
        ('1973-11-01', '1975-03-01'),
        ('1980-01-01', '1980-07-01'),
        ('1981-07-01', '1982-11-01'),
        ('1990-07-01', '1991-03-01'),
        ('2001-03-01', '2001-11-01'),
        ('2007-12-01', '2009-06-01'),
        ('2020-02-01', '2020-04-01')
    ]

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FRED API client

        Args:
            api_key: FRED API key. If None, will try to read from environment variable
        """
        if api_key is None:
            api_key = os.getenv('FRED_API_KEY')

        if not api_key:
            raise ValueError(
                "FRED API key not found. Please provide an API key or set FRED_API_KEY environment variable.\n"
                "Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html"
            )

        self.fred = Fred(api_key=api_key)

    def fetch_series(self,
                    series_id: str,
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None) -> pd.Series:
        """
        Fetch a single economic series from FRED

        Args:
            series_id: FRED series identifier
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format

        Returns:
            pandas Series with the data
        """
        try:
            data = self.fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
            return data
        except Exception as e:
            print(f"Error fetching {series_id}: {str(e)}")
            return pd.Series()

    def fetch_multiple_series(self,
                             series_ids: List[str],
                             start_date: Optional[str] = None,
                             end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch multiple economic series and combine into a DataFrame

        Args:
            series_ids: List of FRED series identifiers
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format

        Returns:
            pandas DataFrame with all series
        """
        data_dict = {}

        for series_id in series_ids:
            series_data = self.fetch_series(series_id, start_date, end_date)
            if not series_data.empty:
                data_dict[series_id] = series_data

        if not data_dict:
            return pd.DataFrame()

        # Combine all series into a single DataFrame
        df = pd.DataFrame(data_dict)
        df.index.name = 'DATE'

        return df

    def calculate_growth_rates(self, df: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
        """
        Calculate year-over-year or period-over-period growth rates

        Args:
            df: DataFrame with economic data
            periods: Number of periods for growth calculation (12 for YoY with monthly data)

        Returns:
            DataFrame with growth rates
        """
        growth_df = pd.DataFrame(index=df.index)

        for col in df.columns:
            growth_df[f'{col}_growth'] = ((df[col] - df[col].shift(periods)) / df[col].shift(periods)) * 100

        return growth_df

    def get_latest_values(self, series_ids: List[str]) -> Dict[str, Dict]:
        """
        Get the most recent value and date for each series

        Args:
            series_ids: List of FRED series identifiers

        Returns:
            Dictionary with series_id: {'value': float, 'date': timestamp}
        """
        latest_values = {}

        for series_id in series_ids:
            try:
                # Get data from the last 180 days to ensure we capture quarterly data
                end_date = datetime.now()
                start_date = end_date - timedelta(days=180)

                series_data = self.fetch_series(
                    series_id,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d')
                )

                if not series_data.empty:
                    latest_values[series_id] = {
                        'value': series_data.iloc[-1],
                        'date': series_data.index[-1]
                    }
                else:
                    latest_values[series_id] = None

            except Exception as e:
                print(f"Error getting latest value for {series_id}: {str(e)}")
                latest_values[series_id] = None

        return latest_values

    def get_series_info(self, series_id: str) -> Dict:
        """
        Get metadata information about a series

        Args:
            series_id: FRED series identifier

        Returns:
            Dictionary with series information
        """
        if series_id in self.INDICATORS:
            return self.INDICATORS[series_id]
        else:
            try:
                info = self.fred.get_series_info(series_id)
                return {
                    'name': info.get('title', series_id),
                    'units': info.get('units', 'Unknown'),
                    'seasonal_adj': info.get('seasonal_adjustment', 'Unknown'),
                    'frequency': info.get('frequency', 'Unknown')
                }
            except Exception as e:
                print(f"Error getting info for {series_id}: {str(e)}")
                return {'name': series_id, 'units': 'Unknown', 'seasonal_adj': 'Unknown', 'frequency': 'Unknown'}
