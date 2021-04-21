from yahoo_fin import stock_info as si
import statsmodels.formula.api as sm
from itertools import accumulate
from datetime import datetime
import pandas as pd
import time
import json

# Define Functions
def regress(List):
    """
    Returns Regression Coefficient ß
    """
    assert type(List) == list
    data = pd.DataFrame()
    data['Y'] = List
    data['X'] = list(range(1, len(List) + 1))
    Y = data.iloc[:, 0].values.reshape(-1, 1)
    X = data.iloc[:, 1].values.reshape(-1, 1)
    result = sm.ols(formula="Y ~ X", data=data).fit()
    result = sm.ols(formula="Y ~ X", data=data).fit()
    coeff = result.params.X
    return coeff

def main(crypto):
    """
    App while loop.

    Parameter crypto: the crypto currency to get data on.
    """
    APP = True
    while APP == True:

        ETH = si.get_live_price("ETH-USD")
        print(ETH)
        ETH_accum = [ETH] + ETH_accum

        if len(ETH_accum) >= 120:

            #Splits the queue into 6 smaller ones
            split_length = [20, 20, 20, 20, 20, 20]
            reg_list = [ETH_accum[x - y: x] for x, y in zip(accumulate(split_length), split_length)]

            ETH_betas = []
            for section in reg_list:
                value = regress(section)
                if value != None:
                    ETH_betas.append(value)
                else:
                    ETH_betas.append(0)

            #Analyze regression findings
            #Should we weight the magnitude/difference between first and last?
            recent = ETH_betas[0] < 0 and ETH_betas[1] < 0
            midterm = ETH_betas[2] < 0 and ETH_betas[3] < 0
            old = ETH_betas[4] < 0 and ETH_betas[4] < 0

            #Make the actual trades
            if recent and midterm and not old:
                HISTORY = HISTORY.append([now, 'BUY', ETH])
            elif not recent and not midterm and old:
                HISTORY = HISTORY.append([now, 'SELL', ETH])
            else:
                HISTORY = HISTORY.append([now, 'HOLD', ETH])

            ETH_accum.pop(-1)
            # HISTORY.to_csv("../TrainData/HISTORY.csv")
        time.sleep(30)

# Accumulators & History


# need way to retrieve data and run regression
# need regression model/ decision making process
# need to train/test model
    # to start, lets get historical data a run our model on it. call generic buy hold sell fucntion
    # and we have see how much we would have made/lost in that window




# need to actuallly make trades
# need to connect to server



# https://pypi.org/project/yahoo-finance/
# https://github.com/jmfernandes/robin_stocks
