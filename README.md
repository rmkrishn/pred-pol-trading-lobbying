# lobbying-to-stocktrades
This is an ongoing data science project, studying the influence that lobbying efforts have on the trading of individual stocks by politicians.

There are a number of Jupyter notebooks visible, which detail our some of our methods and process. For the most part, these need to be better organized and edited, but please take a look.

There are a number of folders containing the relevant data analyzed in this project. The lobbying data may be found in "lobbying_data"; data on politician stock trades can be found in "trading_data."

Lobbying data is mainly sourced directly from the Office of the Senate. There are a few different forms of it available on this repository. First, it can be found in a single raw .csv called "filings_all.csv". It has also been split up by issue code and by quarter - see the subfolders "by_issue_code" and "by_quarter". We have downloaded filings running from 2013 to the end of 2023 (we may update the data set with Q1 2024 filings as well, but this is still to be determined.)
There is also some lobbying data sourced from opensecrets.org. This data was largely un-used in this project, but may be useful for further inquiry.

Trading data is sourced from QuiverQuant, and can be found in the file "congress-trading-all.xlsx". There are also a number of useful .csv files in the "trading_data" folder that help to match lobbying issues with stock sectors.

Finally, there are a few python scripts in the "scripts" folder. These are used throughout the Jupyter notebooks.