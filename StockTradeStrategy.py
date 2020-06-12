#Dual Moving Crossover

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from fastquant import get_pse_data
from MovingAverage import MovingAverage
from RSI import RSI

class Main():

    def __init__(self,StockCode, StartDate, EndDate):
        df = get_pse_data(StockCode, StartDate, EndDate)

        # Derive the 30 day SMA of JFC's closing prices
        ma30 = df.close.rolling(30).mean()
        ma100 = df.close.rolling(100).mean()
        # Combine the closing prices with the 30 day SMA
        data = pd.concat([df.close, ma30, ma100], axis=1).dropna()
        data.columns = ['Closing Price', 'Simple Moving Average (30 day)','Simple Moving Average (100 day)']

        #Create a new dataframe
        signal = pd.DataFrame(index=df['close'].index)
        signal['close'] = data['Closing Price']
        signal['SMA30'] = data['Simple Moving Average (30 day)']
        signal['SMA100'] = data['Simple Moving Average (100 day)']


        v_RSI=RSI.getRSI(self, signal)
        MA = MovingAverage.buy_sell(signal)
        signal['Buy_Signal_Price_MA'] = MA[0]
        signal['Sell_Signal_Price_MA'] = MA[1]
        signal['Buy_Signal_Price_RSI']=v_RSI[0]
        signal['Sell_Signal_Price_RSI'] = v_RSI[1]



        # Visually Show The Stock buy and sell signals
        # Create the title
        title = 'Adj. Close Price History Buy / Sell Signals   '
        # Get the stocks
        my_stocks = signal
        ticker = "close"

        # Create and plot the graph
        plt.figure(figsize=(12.2, 4.5))  # width = 12.2in, height = 4.5
        plt.scatter(my_stocks.index, my_stocks['Buy_Signal_Price_MA'], color='green', label='Buy Signal MA', marker='^',
                    alpha=1)
        plt.scatter(my_stocks.index, my_stocks['Sell_Signal_Price_MA'], color='darkred', label='Sell Signal MA', marker='v',
                    alpha=1)
        plt.scatter(my_stocks.index, my_stocks['Buy_Signal_Price_RSI'], color='blue', label='Buy Signal RSI', marker='^',
                    alpha=1)
        plt.scatter(my_stocks.index, my_stocks['Sell_Signal_Price_RSI'], color='red', label='Sell Signal RSI', marker='v',
                    alpha=1)
        plt.plot(my_stocks[ticker], label=ticker,
                 alpha=0.35)  # plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
        plt.plot(my_stocks['SMA30'], label='SMA30', alpha=0.35)
        plt.plot(my_stocks['SMA100'], label='SMA100', alpha=0.35)
        plt.title(title)
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Adj. Close Price PHP', fontsize=18)
        plt.legend(loc='upper left')
        plt.show()

if __name__ == '__main__':
    StockCode="AC"
    StartDate="2018-01-01"
    EndDate="2020-06-10"
    Main(StockCode, StartDate, EndDate)