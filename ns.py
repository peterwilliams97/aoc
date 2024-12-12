from types import SimpleNamespace

stock_dict = {
    "ticker": "TSLA",
    "open": 124.65,
    "previous_close": 124.65,
    "trade_high": 124.67,
    "trade_low": 122.97,
    "year_high": 129.03,
    "year_low": 83.34,
    "dividend_yield": None,
    "currency": "USD"
}

stock = SimpleNamespace(**stock_dict)

print(f"{stock.ticker} opened at {stock.open} {stock.currency}")
print(type(stock))
print(stock.__dict__)
