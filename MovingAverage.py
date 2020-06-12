import numpy as np

class MovingAverage():
    def __init__(self, signal):
        self.buy_sell(signal)
        pass
    # Create a function to signal when to buy and sell an asset
    def buy_sell(signal):
        sigPriceBuy = []
        sigPriceSell = []
        flag = -1
        for i in range(0, len(signal)):
            # if sma30 > sma100  then buy else sell
            if signal['SMA30'][i] > signal['SMA100'][i]:
                if flag != 1:
                    sigPriceBuy.append(signal['close'][i])
                    sigPriceSell.append(np.nan)
                    flag = 1
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
                #print('Buy')
            elif signal['SMA30'][i] < signal['SMA100'][i]:
                if flag != 0:
                    sigPriceSell.append(signal['close'][i])
                    sigPriceBuy.append(np.nan)
                    flag = 0
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
                #print('sell')
            else:  # Handling nan values
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
            #print(signal['SMA30'][i], ':::', signal['SMA100'][i], ':::', flag)
        return (sigPriceBuy, sigPriceSell)


if __name__ == '__main__':
    MovingAverage()
