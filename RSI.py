import pandas as pd
import numpy as np

class RSI():

    def __init__(self, signal):
        self.getRSI(signal)
        pass

    def getRSI(self, signal):
        sigPriceBuy = []
        sigPriceSell = []
        flag = -1
        rsi_period = 14
        chg = signal['close'].diff()
        gain = chg.mask(chg < 0, 0)
        signal['gain'] = gain
        loss = chg.mask(chg > 0, 0)
        signal['loss'] = loss
        avg_gain = gain.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        avg_loss = loss.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        signal['avg_gain'] = avg_gain
        signal['avg_loss'] = avg_loss
        rs = abs(avg_gain / avg_loss)
        rsi = 100 - (100 / (1 + rs))
        signal['rsi'] =rsi
        #print(signal['rsi'])
        for i in range(0, len(signal['rsi'])):
            # if sma30 > sma100  then buy else sell
            if signal['rsi'][i] < 30:
                if flag != 1:
                    sigPriceBuy.append(signal['close'][i])
                    sigPriceSell.append(np.nan)
                    flag = 1
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
                # print('Buy')
            elif signal['rsi'][i] > 70:
                if flag != 0:
                    sigPriceSell.append(signal['close'][i])
                    sigPriceBuy.append(np.nan)
                    flag = 0
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
                # print('sell')
            else:  # Handling nan values
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)

        return (sigPriceBuy, sigPriceSell)


        pass


if __name__ == '__main__':
    RSI(signal)