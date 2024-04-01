import pandas as pd

def normalize_name(name):
    """Convert names in "Lastname, Firstname" format to "Firstname Lastname"."""
    if "," in name:
        return name.split(",")[1].strip() + " " + name.split(",")[0].strip()
    return name.strip()

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

    # Remove a garbled row
    stocks = stocks.drop(42546, axis=0)

    # Parse trade sizes
    stocks["Min_Trade_Size"] = stocks.Trade_Size_USD.map(min_trade_size)
    stocks["Max_Trade_Size"] = stocks.Trade_Size_USD.map(max_trade_size)
    
    # Normalize names
    stocks["Name"] = stocks.Name.map(normalize_name)

    # Drop useless columns
    stocks = stocks.drop(
        ["Status", "Quiver_Upload_Time", "last_modified", "Trade_Size_USD"], axis=1
    )
    return stocks
