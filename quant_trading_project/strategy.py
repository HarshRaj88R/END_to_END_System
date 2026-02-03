import pandas as pd


def generate_ma_crossover(
    df: pd.DataFrame,
    fast_window: int = 20,
    slow_window: int = 60,
) -> pd.DataFrame:
    df = df.copy()

    df["MA_FAST"] = df["Close"].rolling(fast_window).mean()
    df["MA_SLOW"] = df["Close"].rolling(slow_window).mean()

    df["signal"] = 0
    df.loc[df["MA_FAST"] > df["MA_SLOW"], "signal"] = 1

    df["position"] = df["signal"].diff().fillna(0)

    return df
