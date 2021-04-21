import pandas as pd
from globals import *
import getHistData as ghd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

def convertDF():
    """
    Converts all csvs back to df and joins them all. This requires
    they are all on the SAME time series.
    """
    iter = 0
    for ticker in tickers_test:
        df = pd.read_csv("./historical/" +ticker+ ".csv")

        if iter == 0:
            accum = df
        else:
            accum = df.merge(accum, how='outer', left_index=True, right_index=True)
        iter +=1

    return accum.reindex(index=accum.index[::-1])

def regress(df):
    """
    Returns Regression Coefficient ß

    Takes in df of ticker prices, returns merged df with coeff

    Window is global
    """
    old = df
    length = len(df)%window
    data = df.iloc[0: len(df) - length].dropna()
    data['betas'] = 0

    for i in range(0, len(data) - window, window):
        Y = data.loc[data.index[i: i + window], '0']
        Y = Y.values.tolist()
        X = list(range(0, len(Y)))
        df = pd.DataFrame({"Y": Y, "X": X})
        result = sm.ols(formula="Y ~ X", data=df).fit()
        coeff = result.params.X
        data.loc[data.index[i: i + window], 'betas'] = coeff

# add new column that checks if greater than 0 or not
    data['check'] = False
    for i in range(len(data)):
        if data.loc[data.index[i], 'betas'] > 0:
            data.loc[data.index[i], 'check'] = True
    data = data.merge(old, how='outer', left_index=True, right_index=True)
    data = data[data.index % window == 0]
    return data


def convertToDecisions(data):
    """
    data is the pd dataframe. Iterates through df to return array of trade decisions
    """
    decisions = []
    for i in range(0, len(data)-3, 3):
        price = data.loc[data.index[i], '0_y']
        if i == 0:
            decisions.append(["Start", price])
            continue
        if i < 3:
            decisions.append(["H", price])
            continue

        i1 = (data.loc[data.index[i], 'check'] == True)
        i2 = (data.loc[data.index[i-1], 'check'] == True)
        i3 = (data.loc[data.index[i-2], 'check'] == True)

        if i1 + i2 + i3 == 3:
            decisions.append(["B", price])
        elif i1 + i2 + i3 == 0:
            decisions.append(["S", price])
        else:
            decisions.append(["H", price])
    return decisions


def testTrader(decisions, c, guardb, guards):
    """
    @param capital is the amount invested
    @param bguard is the prop of the account to buy when trade is made.
    @param sguard is the prop of shares to sell when trade is made

    Returns nested list of trade evaluations.
    """
    # Initialize the trading - i.e if I bought at time 0, where would I be now?
    start_price = decisions[0][1]
    shares = guardb*c/start_price
    capital = c - guardb*c
    history = []
    history.append([capital, str(shares) + " shares bought at $" + str(start_price)])

    for trade in decisions[1:-1]:
        if trade[0] == "":
            shares = shares + guardb*capital/trade[1]
            capital = capital - guardb*capital
            history.append([capital, str(shares) + " shares bought at $" + str(trade[1])])
        elif trade[0] == "S" and shares > 0:
            capital = capital + guards*shares*trade[1]
            history.append([capital, str(guards*shares) + " shares sold at $" + str(trade[1])])
            shares = shares - guards*shares

    history.append([capital, "Plus " + str(shares*decisions[-1][1]) + " in shares"])
    earnings = capital + shares*decisions[-1][1]  - c
    return [capital + shares*decisions[-1][1], history, earnings]

def visualize(d):
    """
    Parameter d is the dataframe
    """
    plt.scatter(d.index, d['0_y'])
    plt.show()


if __name__ == '__main__':
    ghd.do()
    x = convertDF()
    data = regress(x).dropna()
    print("  ")
    decisions = convertToDecisions(data)
    EARNINGS = testTrader(decisions, 1000, 0.6, 0.9)

    for event in EARNINGS[1]:
        print(event)
    print("  ")
    print("$" + str(EARNINGS[0]) + " in capital. " + str(EARNINGS[2]) + " in earnings.")

    for el in decisions:
        print(el)

    # visualize(data)
    print("  ")


    # try different log or exp reg models
    # try if price is over under some threshold, buy v sell
