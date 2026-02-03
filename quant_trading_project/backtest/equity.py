import pandas as pd


def equity_curve_and_drawdown(trades: pd.DataFrame):
    if trades.empty:
        return pd.DataFrame(), 0.0

    # RESET INDEX TO AVOID ALIGNMENT BUG
    trades = trades.reset_index(drop=True)

    equity = trades["pnl"].cumsum()

    equity_df = pd.DataFrame(
        {
            "equity": equity.values
        },
        index=pd.to_datetime(trades["exit_date"]),
    )

    running_max = equity_df["equity"].cummax()
    drawdown = equity_df["equity"] - running_max

    max_drawdown = drawdown.min()

    return equity_df, float(max_drawdown)
