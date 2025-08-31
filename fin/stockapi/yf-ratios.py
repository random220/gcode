import yfinance as yf
tickers = ["AAPL", "MSFT", "GOOGL"]
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        pe_ratio = stock.info["trailingPE"]
        print(f"P/E Ratio for {ticker}: {pe_ratio:.2f}")
    except (KeyError, IndexError) as e:
        print(f"P/E Ratio for {ticker}: Error retrieving data - {str(e)}")
