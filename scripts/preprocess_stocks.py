from pathlib import Path
import pandas as pd

def normalize_name(name):
    """Convert names in "Lastname, Firstname" format to "Firstname Lastname",
    and remove titles."""
    if "," in name:
        name = name.split(",")[1].strip() + " " + name.split(",")[0].strip()
    name = name.strip()
    if name.startswith("Mr.") or name.startswith("Ms.") or name.startswith("Dr."):
        name = name[3:].strip()
    if name.startswith("Mrs."):
        name = name[4:].strip()
    return name


def normalize_ticker_symbol(symbol):
    """Remove suffixes for classes of stock, foreign stocks, etc."""
    if "$" in symbol:
        symbol = symbol[:symbol.find("$")]
    if "." in symbol:
        symbol = symbol[:symbol.find(".")]
    return symbol


def min_trade_size(size):
    """Extract minimum value of trade size range."""
    if "-" in size:
        size = size.split("-")[0].strip()
    size = size.replace("$", "").replace(",", "")
    return float(size)


def max_trade_size(size):
    """Extract maximum value of trade size range."""
    if "-" in size:
        size = size.split("-")[1].strip().strip(".")
    size = size.replace("$", "").replace(",", "")
    return float(size)


def get_all_codes(row):
    """Assemble all of lobbying codes for each row of the
    sector2lobbyingcode data. Presented as a string so we can use pandas
    string methods.
    """
    cats = []
    for i in range(1, 4):
        cat = row["Category" + str(i)]
        if not pd.isna(cat):
            cats.append(cat)
    return ",".join(cats)


def preprocess_stock_data(stocks):
    """Some cleaning and preprocessing for the stocks data.
    
    Args:
      stocks (pd.DataFrame): DataFrame loaded from the trading data.
      
    Returns:
      cleaned copy of stocks.
    """
    # Parse dates
    for datetime_col in ["Traded", "Filed", "Quiver_Upload_Time", "last_modified"]:
        stocks[datetime_col] = pd.to_datetime(stocks[datetime_col])

    # Remove some garbled rows
    stocks = stocks.drop(44837, axis=0)
    stocks = stocks.drop(42546, axis=0)
    stocks = stocks.drop(9565, axis=0)

    # Parse trade sizes
    stocks["Min_Trade_Size"] = stocks.Trade_Size_USD.map(min_trade_size)
    stocks["Max_Trade_Size"] = stocks.Trade_Size_USD.map(max_trade_size)
    
    # Normalize names
    stocks["Name"] = stocks.Name.map(normalize_name)

    # Drop useless columns
    stocks.drop([
        "Status", "Quiver_Upload_Time", "excess_return", "last_modified", "Trade_Size_USD"
    ], axis=1, inplace=True)
    # Drop rows that aren't stock or options trades
    stocks.drop(stocks[stocks.TickerType.isin([
        'CS', 'GS', 'AB', 'ET', 'HN', 'Corporate Bond', 'PS',
        'Cryptocurrency', 'OI', 'OL', 'SA'
    ])].index, axis=0, inplace=True)
    
    # Clean up ticker symbols
    stocks["Ticker"] = stocks.Ticker.map(normalize_ticker_symbol)
    
    # Renamed ticker symbols: Meta, Raytheon, ...
    stocks["Ticker"] = stocks.Ticker.replace(
        ["FB", "UTX", "RTN", "FISV"],
        ["META", "RTX", "RTX", "FI"]
    )
    
    # Combine House and Senate naming styles for TickerType
    stocks["TickerType"] = stocks.TickerType.replace(
        ["Stock", "Stock Option", "Other Securities"],
        ["ST", "OP", "OT"],
    )
    
    # Get quarter
    stocks["Quarter"] = pd.PeriodIndex(stocks["Filed"], freq="Q")
    
    stocks.sort_values(by="Filed", inplace=True)
    return stocks


def merge_and_clean_stock_data(data_dir):
    """Clean the stock data, filter down so that only stocks are represented,
    and merge with sector/lobbying code info.
    
    Args:
      data_dir (str or pathlike): Directory where data tables are stored.
      
    Returns:
      A DataFrame holding all the data.
    """
    data_dir = Path(data_dir)
    stocks = pd.read_excel(data_dir/"congress-trading-all.xlsx",
                           parse_dates=["Traded", "Filed", "Quiver_Upload_Time"])
    stocks = preprocess_stock_data(stocks)
    
    symbol2sector = pd.read_csv(data_dir/"symbol2sector.csv")
    stocks = pd.merge(stocks, symbol2sector, on="Ticker", how="left")
    # Filter to stocks for which Yahoo Finance could find sector/industry data
    stocks.drop(stocks[stocks.YFQuoteType != "EQUITY"].index, axis=0, inplace=True)
    
    sector2code = pd.read_csv(data_dir/"sector2lobbyingcode.csv")
    stocks = pd.merge(stocks, sector2code, on="Industry", how="left")
    stocks["Codes"] = stocks.apply(get_all_codes, axis=1)
    stocks.loc[:, "Codes"] = stocks.Codes.fillna("")
    
    return stocks

if __name__ == "__main__":
    stocks = merge_and_clean_stock_data("trading_data")
    
    stocks.to_csv("trading_data/stocks_cleaned.csv", index=False)
    print("Wrote cleaned stock data.")