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
    if "-" in size:
        size = size.split("-")[0].strip()
    size = size.replace("$", "").replace(",", "")
    return float(size)


def max_trade_size(size):
    if "-" in size:
        size = size.split("-")[1].strip().strip(".")
    size = size.replace("$", "").replace(",", "")
    return float(size)


def preprocess_stock_data(stocks):
    # Parse dates
    for datetime_col in ["Traded", "Filed", "Quiver_Upload_Time", "last_modified"]:
        stocks[datetime_col] = pd.to_datetime(stocks[datetime_col])

    # Remove some garbled rows
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
    return stocks
