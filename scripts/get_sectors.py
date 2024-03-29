import pandas as pd
import yfinance as yf


def sector(ticker_symbol):
    try:
        return yf.Ticker(ticker_symbol).info["sector"]
    except KeyError:
        print(yf.Ticker(ticker_symbol).info)
        return "Not Found"
    except Exception as e:
        print(e)
        return "Not Found"


def industry(ticker_symbol):
    try:
        return yf.Ticker(ticker_symbol).info["industry"]
    except KeyError:
        print(yf.Ticker(ticker_symbol).info)
        return "Not Found"
    except Exception as e:
        print(e)
        return "Not Found"


if __name__ == "__main__":
    stocks = pd.read_excel("../trading_data/congress-trading-all.xlsx")
    symbol2sector = {}
    for i, ticker_symbol in enumerate(stocks.Ticker.unique()):
        symbol2sector[ticker_symbol] = [sector(ticker_symbol), industry(ticker_symbol)]
        print(ticker_symbol, *symbol2sector[ticker_symbol])
        # sleep(0.5)
    sectors_df = pd.DataFrame.from_dict(symbol2sector, orient="index",
                                        columns=["sector", "industry"])
    sectors_df.to_csv("../trading_data/symbol2sector.csv")
    print("Wrote to ../trading_data/symbol2sector.csv")
