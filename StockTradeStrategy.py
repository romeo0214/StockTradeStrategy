#Dual Moving Crossover

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from fastquant import get_pse_data
from MovingAverage import MovingAverage
from RSI import RSI
from tkinter import *
from tkinter import scrolledtext

class Main():

    def __init__(self,StockCode, StartDate, EndDate):
        log_txt.insert(INSERT, 'getting price list\n')
        try:
            df = get_pse_data(StockCode, StartDate, EndDate)
        except Exception as e:
            log_txt.insert(INSERT, 'Get pse data error: {e}\n'.format(e=e))


        log_txt.insert(INSERT, 'price list obtained')

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

        log_txt.insert(INSERT, 'calculate RSI\n')
        v_RSI=RSI.getRSI(self, signal)
        log_txt.insert(INSERT, 'done calculating RSI\n')
        log_txt.insert(INSERT, 'calculate moving averages\n')
        MA = MovingAverage.buy_sell(signal)
        log_txt.insert(INSERT, 'done calculating moving averages\n')

        try:
            signal['Buy_Signal_Price_MA'] = MA[0]
            signal['Sell_Signal_Price_MA'] = MA[1]
            signal['Buy_Signal_Price_RSI']=v_RSI[0]
            signal['Sell_Signal_Price_RSI'] = v_RSI[1]
        except Exception as e:
            log_txt.insert(INSERT, 'Get buy and sell data error: {e}\n'.format(e=e))



        # Visually Show The Stock buy and sell signals
        # Create the title

        title = 'Adj. Close Price History Buy / Sell Signals   '
        # Get the stocks
        my_stocks = signal
        ticker = "close"

        # Create and plot the graph
        try:
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
        except Exception as e:
            log_txt.insert(INSERT, 'Plotting data error: {e}\n'.format(e=e))
        try:
            plt.show()
        except Exception as e:
            log_txt.insert(INSERT, 'Plotting data error: {e}\n'.format(e=e))
        log_txt.insert(INSERT, 'Produced graph\n')

if __name__ == '__main__':
    

    window = Tk()
    window.title("Stock Trade Strategy")
    window.geometry('350x200')
    lbl = Label(window, text="Stock Code")
    lbl.grid(column=0, row=0)
    StockCode_txt = Entry(window, width=10)
    StockCode_txt.grid(column=1, row=0)
    StockCode_lbl = Label(window, text="Stock Code")
    StockCode_lbl.grid(column=0, row=1)

    StartDate_txt = Entry(window, width=10)
    StartDate_txt.grid(column=1, row=1)
    StartDate_lbl = Label(window, text="Start Date (YYYY-MM-DD)")
    StartDate_lbl.grid(column=0, row=1)

    EndDate_txt = Entry(window, width=10)
    EndDate_txt.grid(column=1, row=2)
    EndDate_lbl = Label(window, text="End Date (YYYY-MM-DD)")
    EndDate_lbl.grid(column=0, row=2)

    log_txt = scrolledtext.ScrolledText(window, width=40, height=6)
    log_txt.grid(column=0, row=4, columnspan=2)

    def clicked():
        StockCode = StockCode_txt.get()
        StartDate = StartDate_txt.get()
        EndDate = EndDate_txt.get()
        log_txt.insert(INSERT, 'Running for: {StockCode}\n'.format(StockCode=StockCode))
        log_txt.insert(INSERT, 'StartDate: {StartDate}\n'.format(StartDate=StartDate))
        log_txt.insert(INSERT, 'EndDate: {EndDate}\n'.format(EndDate=EndDate))

        Main(StockCode, StartDate, EndDate)

    btn = Button(window, text="Run", command=clicked)
    btn.grid(column=0, row=3)

    window.mainloop()


