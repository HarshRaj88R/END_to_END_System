from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd

from data.market_data import fetch_daily_data
from backtest.data_split import split_data
from strategy import generate_ma_crossover
from backtest.backtester import backtest_long_only
from forward_test.engine import forward_test_long_only
from backtest.metrics import compute_metrics
from backtest.equity import equity_curve_and_drawdown

app = FastAPI(title="Quant Trading API")


# -----------------------
# MODELS
# -----------------------

class OrderRequest(BaseModel):
    symbol: str
    side: str   # BUY or SELL
    quantity: int


# -----------------------
# CORE PIPELINE (REUSED)
# -----------------------

def run_pipeline(symbol: str = "AAPL"):
    df = fetch_daily_data(symbol)

    backtest_df, forward_df = split_data(df)

    backtest_df = generate_ma_crossover(backtest_df)
    forward_df = generate_ma_crossover(forward_df)

    bt_trades = backtest_long_only(backtest_df)
    fw_trades, _ = forward_test_long_only(forward_df)

    fw_trades_df = pd.DataFrame(fw_trades)

    bt_metrics = compute_metrics(bt_trades)
    fw_metrics = compute_metrics(fw_trades_df)

    bt_equity, bt_dd = equity_curve_and_drawdown(bt_trades)
    fw_equity, fw_dd = equity_curve_and_drawdown(fw_trades_df)

    latest_signal = int(forward_df.iloc[-1]["position"])

    return {
        "backtest_metrics": bt_metrics,
        "forward_metrics": fw_metrics,
        "backtest_drawdown": bt_dd,
        "forward_drawdown": fw_dd,
        "latest_signal": latest_signal,
    }


# -----------------------
# ENDPOINTS
# -----------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    """
    Returns backtest & forward test metrics.
    """
    data = run_pipeline()
    return {
        "backtest": data["backtest_metrics"],
        "forward": data["forward_metrics"],
    }


@app.get("/signal")
def signal():
    """
    Returns latest strategy signal.
    """
    data = run_pipeline()

    signal_map = {
        1: "BUY",
        -1: "SELL",
        0: "HOLD",
    }

    return {
        "signal": signal_map[data["latest_signal"]]
    }


@app.post("/order")
def place_order(order: OrderRequest):
    """
    Paper order validation using strategy signal.
    """
    data = run_pipeline()

    signal = data["latest_signal"]

    if order.side == "BUY" and signal != 1:
        return {"status": "rejected", "reason": "No BUY signal"}

    if order.side == "SELL" and signal != -1:
        return {"status": "rejected", "reason": "No SELL signal"}

    return {
        "status": "accepted",
        "symbol": order.symbol,
        "side": order.side,
        "quantity": order.quantity,
    }
