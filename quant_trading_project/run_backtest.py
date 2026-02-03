import pandas as pd
from data.market_data import fetch_daily_data
from backtest.data_split import split_data
from strategy import generate_ma_crossover
from backtest.backtester import backtest_long_only
from forward_test.engine import forward_test_long_only
from backtest.metrics import compute_metrics
from backtest.equity import equity_curve_and_drawdown


# FETCH DATA
df = fetch_daily_data("AAPL")

# SPLIT DATA
backtest_df, forward_df = split_data(df)

# GENERATE SIGNALS
backtest_df = generate_ma_crossover(backtest_df)
forward_df = generate_ma_crossover(forward_df)

# ===== BACKTEST =====
bt_trades = backtest_long_only(backtest_df)

print("BACKTEST METRICS")
print(compute_metrics(bt_trades))

bt_equity, bt_max_dd = equity_curve_and_drawdown(bt_trades)
print("\nBACKTEST EQUITY (LAST 5)")
print(bt_equity.tail())
print("BACKTEST MAX DRAWDOWN:", bt_max_dd)

# ===== FORWARD TEST =====
fw_trades, fw_pnl = forward_test_long_only(forward_df)
fw_trades_df = pd.DataFrame(fw_trades)

print("\nFORWARD TEST METRICS")
print(compute_metrics(fw_trades_df))

fw_equity, fw_max_dd = equity_curve_and_drawdown(fw_trades_df)
print("\nFORWARD TEST EQUITY (LAST 5)")
print(fw_equity.tail())
print("FORWARD TEST MAX DRAWDOWN:", fw_max_dd)
