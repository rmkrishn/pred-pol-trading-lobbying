import pandas as pd
import yfinance as yf
from tqdm import tqdm
from preprocess_stocks import preprocess_stock_data


def query_yf(ticker_symbol, keys):
    """Try to extract keys from Yahoo Finance information on ticker symbol.
    Return "Not Found" if an error is thrown.
    
    Args:
      ticker_symbol (str): Ticker symbol to search for.
      keys (str or list of str): Key or list of keys to obtain.
      
    Returns:
      List of results, of the same length as that of keys.
    """
    if isinstance(keys, str):
        keys = [keys]
    try:
        info = yf.Ticker(ticker_symbol).info
    except Exception as e:
        print(e)
        return ["Not Found" for _ in range(len(keys))]
    results = []
    for key in keys:
        if key not in info:
            results.append("Not Found")
        else:
            results.append(info[key])
    return results

if __name__ == "__main__":
    stocks = pd.read_excel("../trading_data/congress-trading-all.xlsx")
    stocks = preprocess_stock_data(stocks)
    symbol2sector = {}
    for ticker_symbol in tqdm(stocks.Ticker.unique(), total=len(stocks.Ticker.unique())):
        symbol2sector[ticker_symbol] = query_yf(
            ticker_symbol, ["sector", "industry", "quoteType"]
        )
    sectors_df = pd.DataFrame.from_dict(
        symbol2sector, orient="index", columns=["Sector", "Industry", "YFQuoteType"]
    )
    sectors_df.index.name = "Ticker"
    sectors_df.to_csv("../trading_data/symbol2sector.csv")
    print("Wrote to ../trading_data/symbol2sector.csv")
