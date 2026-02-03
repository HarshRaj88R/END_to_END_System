import pandas as pd


def split_data(df: pd.DataFrame, ratio: float = 0.5):
    split_index = int(len(df) * ratio)
    return df.iloc[:split_index].copy(), df.iloc[split_index:].copy()
