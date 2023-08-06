import ta
import pandas as pd
import numpy as np

class data_treatment:
        
    def resample_df(self, period, data):
        
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
    
    def obv(self, df):
        
        data = df.copy()
        
        first_cond = data['close']>data['close'].shift(1)
        second_cond = data['close']<data['close'].shift(1)

        obv = np.where(first_cond, data['volume'], np.where(second_cond, -data['volume'], 0)).cumsum()
        
        return obv
    
    
    def add_inds(self, data):

        #Parameter setup

        length = 20
        mult = 2 
        length_KC = 20
        mult_KC = 1.5

        
        df = data.copy()

        #calculate OBV

        df['obv'] = self.obv(df)
        
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

        
        df.dropna(inplace=True)

        return df
    
    def resampled_data(self, tf_list, data):
        d_tf = {}
        for x in tf_list:
            d_tf[x] = self.resample_df(x, data)
            
        return d_tf
    
    def resample_and_ind(self, period, data):
        
        df = self.resample_df(period, data)
        df_ind = self.add_inds(df)
        
        return df_ind