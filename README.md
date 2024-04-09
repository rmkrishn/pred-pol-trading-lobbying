# lobbying-to-stocktrades
This is an ongoing data science project, studying the influence that lobbying efforts have on the trading of individual stocks by politicians.

There are a number of Jupyter notebooks visible, which detail our some of our methods and process.

In addition, there are a number of data folders containing the relevant data analyzed in this project. 

Lobbying data is mainly sourced from the Office of the Senate. In relatively raw form, it may be found via the Google drive link "https://drive.google.com/file/d/1JgM6Y4ymoti5cdVBa_IC8Nmvn21TVTMj/view?usp=sharing". It is divided by year, and individual files within each year correspond to the type of filing. Filenames include the appropriate filing code, which can be read as follows: 

| Code         | Meaning                                          |
| ------------ | ------------------------------------------------ |
| R            | Registration                                     |
| A            | Amendment                                        |
| Number (w/Q) | Quarter                                          |
| Y            | No activity                                      |
| T            | Termination (lobbying for a client has finished) |
| @            | Termination amendment                            |

So, for instance, a code Q2Y lists filings for quarter 2 where there is no activity for the registration (client-lobbyist pair); a code 2@ lists those filings for quarter 2 amending a 2T filing.

Some summary statistics on lobbying data is also available from opensecrets.com, and can be found in the "opensecrets_data" folder. This is essentially useless for most of our analysis.

Stock trading data is sourced from QuiverQuant, and can be found in the "trading_data" folder.