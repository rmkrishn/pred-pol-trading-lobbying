"""Tools for data visualization."""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scripts.data_extraction import stock_and_lobbying_totals


def plot_lobbying_vs_stocks(issue_codes, stock_cats, category_name,
                            adjust_for_num_codes=False):
    totals = stock_and_lobbying_totals(issue_codes, stock_cats,
                                       adjust_for_num_codes=adjust_for_num_codes)
    
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()
    sns.lineplot(totals.lobbying_total, ax=axs[0])
    axs[0].set_ylabel("Total lobbying expenditure")
    axs[0].set_title(f"Lobbying totals")
    axs[0].tick_params(axis="x", rotation=45)
    sns.lineplot(totals.stocks_gross, ax=axs[1])
    axs[1].set_ylabel("Gross trading (USD)")
    axs[1].set_title(f"Gross stock trading")
    axs[1].tick_params(axis="x", rotation=45)
    sns.lineplot(totals.stocks_gross, ax=axs[2])
    axs[2].set_ylabel("Purchases - sales (USD)")
    axs[2].set_title(f"Net stock trading")
    axs[2].tick_params(axis="x", rotation=45)
    sns.lineplot(totals.stocks_gross_frac, ax=axs[3])
    axs[3].set_ylabel("Fraction")
    axs[3].set_title(f"Fraction of gross stock trading")
    axs[3].tick_params(axis="x", rotation=45)
    fig.suptitle(category_name.upper())
    plt.tight_layout()
    