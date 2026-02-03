def forward_test_long_only(df):
    trades = []
    in_position = False
    entry_price = 0.0
    entry_date = None
    realized_pnl = 0.0

    for date, row in df.iterrows():
        if row["position"] == 1 and not in_position:
            in_position = True
            entry_price = row["Close"]
            entry_date = date

        elif row["position"] == -1 and in_position:
            exit_price = row["Close"]
            pnl = exit_price - entry_price
            realized_pnl += pnl

            trades.append(
                {
                    "entry_date": entry_date,
                    "exit_date": date,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "pnl": pnl,
                }
            )
            in_position = False

    # FORCE CLOSE
    if in_position:
        exit_price = df.iloc[-1]["Close"]
        pnl = exit_price - entry_price
        realized_pnl += pnl
        trades.append(
            {
                "entry_date": entry_date,
                "exit_date": df.index[-1],
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": pnl,
            }
        )

    return trades, realized_pnl
