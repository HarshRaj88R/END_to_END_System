import streamlit as st
import pandas as pd

from data.market_data import fetch_daily_data
from backtest.data_split import split_data
from strategy import generate_ma_crossover
from backtest.backtester import backtest_long_only
from forward_test.engine import forward_test_long_only
from backtest.metrics import compute_metrics
from backtest.equity import equity_curve_and_drawdown


st.set_page_config(page_title="Quant Trading Dashboard", layout="wide")

st.title("📈 Quant Trading Dashboard")
st.subheader("MA(20/60) Crossover — AAPL (Daily)")

# -----------------------
# RUN PIPELINE
# -----------------------

df = fetch_daily_data("AAPL")

backtest_df, forward_df = split_data(df)

backtest_df = generate_ma_crossover(backtest_df)
forward_df = generate_ma_crossover(forward_df)

bt_trades = backtest_long_only(backtest_df)
fw_trades, _ = forward_test_long_only(forward_df)
fw_trades_df = pd.DataFrame(fw_trades)

bt_equity, bt_max_dd = equity_curve_and_drawdown(bt_trades)
fw_equity, fw_max_dd = equity_curve_and_drawdown(fw_trades_df)

bt_metrics = compute_metrics(bt_trades)
fw_metrics = compute_metrics(fw_trades_df)

# -----------------------
# METRICS
# -----------------------

st.header("📊 Performance Metrics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Backtest")
    st.json(bt_metrics)
    st.write("Max Drawdown:", bt_max_dd)

with col2:
    st.subheader("Forward Test")
    st.json(fw_metrics)
    st.write("Max Drawdown:", fw_max_dd)

# -----------------------
# EQUITY CURVES
# -----------------------

st.header("📉 Equity Curves")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Backtest Equity Curve")
    st.line_chart(bt_equity)

with col4:
    st.subheader("Forward Test Equity Curve")
    st.line_chart(fw_equity)

st.caption("Built on your MA crossover strategy • No open positions • Clean backtest & forward test")
