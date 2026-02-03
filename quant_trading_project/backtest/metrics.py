import pandas as pd
import numpy as np


def compute_metrics(trades: pd.DataFrame) -> dict:
    if trades.empty:
        return {}

    total_pnl = trades["pnl"].sum()
    wins = trades[trades["pnl"] > 0]
    losses = trades[trades["pnl"] < 0]

    win_rate = len(wins) / len(trades)
    avg_win = wins["pnl"].mean() if not wins.empty else 0.0
    avg_loss = losses["pnl"].mean() if not losses.empty else 0.0

    profit_factor = (
        wins["pnl"].sum() / abs(losses["pnl"].sum())
        if not losses.empty else float("inf")
    )

    return {
        "total_pnl": float(round(total_pnl, 3)),
        "num_trades": int(len(trades)),
        "win_rate": float(round(win_rate, 3)),
        "avg_win": float(round(avg_win, 3)),
        "avg_loss": float(round(avg_loss, 3)),
        "profit_factor": float(round(profit_factor, 3)),
    }
