from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import alpaca_trade_api as tradeapi
import ta
import pandas as pd
import numpy as np
import mplfinance as mpf
import datetime as dt
import pytz
import yfinance as yf


API_KEY = "PKDRSQ2PLZSGM09IATSQ"
SECRET_KEY = "n1B9TVDO5tqiio75qaz8diElQFA4cW7t3L5ccmpI"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, SECRET_KEY, APCA_API_BASE_URL, 'v2')

class data_treatment:
    def __init__(self, data):
        self.data = data
        
    def resample_df(self, period):
        data = self.data
        
        df = data.copy()

        ohlc_dict = {                                                                                                             
            'open': 'first',                                                                                                    
            'high': 'max',                                                                                                       
            'low': 'min',                                                                                                        
            'close': 'last',                                                                                                    
            'volume': 'sum',
        }

        new_df = df.resample(period, closed='left', label='left').apply(ohlc_dict)

        new_df.dropna(inplace=True)

        return new_df
    
    def obv(self):
        data = self.data
        first_cond = data['close']>data['close'].shift(1)
        second_cond = data['close']<data['close'].shift(1)

        obv = np.where(first_cond, data['volume'], np.where(second_cond, -data['volume'], 0)).cumsum()
        return obv
    
    
    def add_inds(self):

        #Parameter setup

        length = 20
        mult = 2 
        length_KC = 20
        mult_KC = 1.5

        data = self.data
        
        df = data.copy()

        # calculate Bollinger Bands
        # moving average
        m_avg = df['close'].rolling(window=length).mean()
        # standard deviation
        m_std = df['close'].rolling(window=length).std(ddof=0)
        # upper Bollinger Bands
        df['upper_BB'] = m_avg + mult * m_std
        # lower Bollinger Bands 
        df['lower_BB'] = m_avg - mult * m_std

        # calculate Keltner Channel
        # first we need to calculate True Range
        df['tr0'] = abs(df["high"] - df["low"])
        df['tr1'] = abs(df["high"] - df["close"].shift())
        df['tr2'] = abs(df["low"] - df["close"].shift())
        df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)
        # moving average of the TR
        range_ma = df['tr'].rolling(window=length_KC).mean()
        # upper Keltner Channel
        df['upper_KC'] = m_avg + range_ma * mult_KC
        # lower Keltner Channel
        df['lower_KC'] = m_avg - range_ma * mult_KC

        # calculate MACD and RSI

        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd()
        df['signal'] = macd.macd_signal()
        df['diff'] = macd.macd_diff()

        df['rsi'] = ta.momentum.rsi(df['close'])
        df['rsi_avg'] = df['rsi'].rolling(window=5).mean()

        # check for 'squeeze'
        df['squeeze_on'] = (df['lower_BB'] > df['lower_KC']) & (df['upper_BB'] < df['upper_KC'])
        df['squeeze_off'] =(df['lower_BB'] < df['lower_KC']) & (df['upper_BB'] > df['upper_KC'])

        # calculate momentum value
        highest = df['high'].rolling(window = length_KC).max()
        lowest = df['low'].rolling(window = length_KC).min()
        m1 = (highest + lowest) / 2
        df['ttm'] = (df['close'] - (m1 + m_avg)/2)
        fit_y = np.array(range(0,length_KC))
        df['ttm'] = df['ttm'].rolling(window = length_KC).apply(lambda x : np.polyfit(fit_y, x, 1)[0] * (length_KC-1) + np.polyfit(fit_y, x, 1)[1], raw=True)

        df['obv'] = self.obv()
        
        df.dropna(inplace=True)

        return df
    
    def resampled_data(self, tf_list):
        d_tf = {}
        for x in tf_list:
            d_tf[x] = self.resample_df(x)
            
        return d_tf
        
    
if __name__ =='__main__':
    
    symbol = 'AAPL'
    data =  api.get_barset(symbols = symbol, timeframe='1D', limit=1000).df
    data = data[symbol].dropna()
    p = data_treatment(data)
    
    ls = ['W', 'M']
    
    df = p.resampled_data(ls)
    print(df)