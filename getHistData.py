import cryptowatch as cw
import pandas as pd
from globals import *

def histData(ticker):
    """
    Parameter minutes: number of historical minutes desired
    Parameter ticker: currency to retrieve candle data on

    Returns dict.
    """
    assert type(ticker) == str

    candles = cw.markets.get(ticker, ohlc=True)
    data = candles.of_1m

    accum = {}
    iter = 0
    for candle in data:
        accum[str(iter)] = [(candle[2] + candle[3])/2]
        iter += 1
    return accum

def convertCSV(d, filename):
    """
    Converts dictionary to csv. Procedure returns csv
    """
    assert type(d) == dict
    assert ".csv" in filename
    df = pd.DataFrame.from_dict(d)
    df = df.T
    df.to_csv(filename, encoding='utf-8', index=False)

def do():
    for ticker in tickers_test:
        x = histData(ticker)
        convertCSV(x, "./historical/" +ticker+ ".csv")
