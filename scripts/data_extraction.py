"""Tools for extracting and filtering lobbying and stocks data."""
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd

LOBBYING_PATH = Path("lobbying_data")
TRADING_PATH = Path("trading_data")
lobbying_data = None

def get_all_lobbying_data(train_only=True):
    df = pd.DataFrame()
    for fname in (LOBBYING_PATH / "by_quarter").glob("*.csv"):
        if train_only and ("2023" in fname.name or "2024" in fname.name):
            continue
        df = pd.concat([df, pd.read_csv(fname)])
    return df

def issue_codes_for_company(company_name, regex=True, cache=True, train_only=True):
    """Get a DataFrame counting issue codes lobbied by a client company.
    
    Names can differ in filings, so it makes sense to search broadly. By
    default, a regex search is performed.
    
    Args:
      company_name (str): Name of company to search for.
      regex (bool, default True): Whether to perform a regex search.
      cache (bool, default True): Whether to cache all lobbying data in memory.
        This is faster, but uses about 3GB of memory.
      train_only (bool, default True): Whether to only get training data (data
        from before 2023).
      
    Returns:
      DataFrame with columns "issue_code" and "count".
    """
    codes_counts = defaultdict(int)
    if cache:
        global lobbying_data
        if lobbying_data is None:
            lobbying_data = get_all_lobbying_data(train_only=train_only)
        df = lobbying_data[
            lobbying_data.client.str.contains(company_name, case=False, regex=regex)
        ]
        for codes in df.issue_codes.apply(eval):
            for code in codes:
                codes_counts[code] += 1
    else:
        for fname in (LOBBYING_PATH / "by_quarter").glob("*.csv"):
            if train_only and ("2023" in fname.name or "2024" in fname.name):
                continue
            df = pd.read_csv(fname)
            df = df[df.client.str.contains(company_name, case=False, regex=regex)]
            for codes in df.issue_codes.apply(eval):
                for code in codes:
                    codes_counts[code] += 1
    return pd.DataFrame(codes_counts.items(), columns=["issue_code", "count"]).sort_values(by="issue_code")
    
def stock_and_lobbying_totals(issue_codes, stock_industries, train_only=True):
    """Form DataFrame with quarterly totals for a given set of issue codes and
    industries.
    
    Monetary totals reported in stock data are coarse. We use the minimum reported
    trade size for every trade, and treat partial sales as equal to full sales.
    
    Args:
      issue_codes (str or list of str): One or more issue codes to look up.
      stock_industries (str or list of str): One or more stock industries to look up.
      train_only (bool, default True): Whether to only use training data (data
        from before 2023).
        
    Returns:
      A DataFrame with the lobbying income and expenses for each quarter, and
        the stock total purchase and sale amounts, as well as gross
        (purchase + sale + exchange) and net (purchase - sale) trading.
    """
    if isinstance(issue_codes, str):
        issue_codes = [issue_codes]
    if isinstance(stock_industries, str):
        stock_industries = [stock_industries]
        
    end_date = "2022-12-31" if train_only else "2024-03-31"
    out = pd.DataFrame(
        index=pd.period_range(start=2013, end=end_date, freq="Q").to_timestamp(),
        columns=["income", "expenses"],
        dtype=np.float64
    )
    out[:] = 0.0
    for code in issue_codes:
        one_issue = pd.read_csv(LOBBYING_PATH / f"by_issue_code/filings_{code}.csv",
                                parse_dates=["dt_posted", "period_start", "period_end"])
        if train_only:
            one_issue = one_issue[one_issue.period_start.dt.year < 2023]
        out += one_issue.groupby("period_start")[["income", "expenses"]].sum()
        
    out.rename(columns=lambda x: "lobbying_"+x, inplace=True)
        
    out["lobbying_total"] = out["lobbying_income"] + out["lobbying_expenses"]
    
    stocks = pd.read_csv(TRADING_PATH / "stocks_cleaned.csv", parse_dates=["Traded", "Filed", "Quarter"])
    if train_only:
        stocks = stocks[stocks.Quarter < pd.to_datetime("2023-01-01", format="%Y-%m-%d")]
    stock_total_trading = stocks.groupby("Quarter")["Min_Trade_Size"].sum()
    filtered = stocks[stocks.Industry.isin(stock_industries)]

    out["stocks_purchase"] = filtered[filtered["Transaction"] == "Purchase"].groupby("Quarter").Min_Trade_Size.sum()
    out["stocks_sale"] = filtered[filtered["Transaction"].str.startswith("Sale")].groupby("Quarter").Min_Trade_Size.sum()
    out["stocks_gross"] = filtered.groupby("Quarter").Min_Trade_Size.sum()
    out["stocks_net"] = out["stocks_purchase"] - out["stocks_sale"]
    out["stocks_gross_frac"] = out["stocks_gross"] / stock_total_trading
    out.fillna(0, inplace=True)
    return out