import yfinance as yf
import pandas as pd


def fetch_daily_data(symbol: str, start: str = "2010-01-01") -> pd.DataFrame:
    df = yf.download(
        symbol,
        start=start,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df.dropna()
