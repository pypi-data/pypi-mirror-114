import numpy as np

'''-------Function to get value of stock price at given index--------'''


def get_value(dataframe, index):
    return dataframe.get_value(index, 'Close')


'''-------Function to get value of rolling mean for a given window size of dataFrame------'''


def get_rolling_mean(values, window):
    return values.rolling(window=window, center=False).mean()


'''-------Function to get rolling standard deviation for a given window size of dataFrame------'''


def get_rolling_std(values, window):
    return values.rolling(window=window, center=False).std()


'''-------Function to get exponential moving average for a given window size of dataFrame------'''


def get_exp_moving_avg(dataframe, window):
    return dataframe.ewm(span=window).mean()


'''-------Function to get momentum of stockprice for a given dataFrame--------'''


def get_momentum(dataframe, length):
    momentum = dataframe.diff(periods=length)
    return momentum


'''-------Function which returns trend direction--------'''


def get_trend_direction(df):
    dfm = df.rolling(window=10, center=False).mean()
    slope = get_momentum(dfm, 1)
    slope_arr = np.array(slope)
    trend_dir = np.average(slope_arr[10:(10 + 10 - 1)])
    return trend_dir


'''--------Function which gives RSI for a given dataFrame--------'''


def get_RSI(df):
    current_data = df['Close']
    rsi = [0] * len(df)

    for i in range(15, len(df)):
        data_req = current_data[i - 15:i]
        change = data_req.diff()
        data_len = len(change)
        change = change.fillna(method='bfill')
        change = np.array(change)
        pos_gain = 0
        neg_loss = 0

        for j in range(data_len):
            if change[j] >= 0:
                pos_gain = pos_gain + change[j]
            else:
                neg_loss = neg_loss - change[j]

        if neg_loss == 0:
            rsi[i] = 100
        else:
            gtol_ratio = pos_gain / neg_loss
            rsi[i] = 100 - (100 / (1 + gtol_ratio))
    return rsi


'''--------Function which gives Bollinger bands for a given dataFrame--------'''


def get_bollinger_bands(dataframe):
    rolling_mean = get_rolling_mean(dataframe['Close'], 20)
    rolling_std_dev = get_rolling_std(dataframe['Close'], 20)

    upper_bollinger_band = rolling_mean + 2 * rolling_std_dev
    lower_bollinger_band = rolling_mean - 2 * rolling_std_dev

    return upper_bollinger_band, lower_bollinger_band


'''--------Function which returns MACD for a given dataFrame--------'''


def get_MACD(df):
    ema_12 = get_exp_moving_avg(df['Close'], 12)
    ema_26 = get_exp_moving_avg(df['Close'], 26)
    macd_line = ema_12 - ema_26
    signal_line = get_exp_moving_avg(macd_line, 9)
    macd_hist = macd_line - signal_line

    return macd_hist


'''-------Function which Returns CCI for a given dataFrame---------'''


def get_cci(df):
    cci = [0] * len(df)
    typical_price = (df['High'] + df['Close'] + df['Low']) / 3

    for i in range(15, len(typical_price)):
        tp_req = typical_price[i - 15:i]
        tp_req = np.array(tp_req)
        sma = np.average(tp_req)
        sma = [sma] * 15
        mean_deviation = np.sum(abs(tp_req - sma)) / 14
        cci[i] = (tp_req[14] - np.average(tp_req)) / (0.015 * mean_deviation)

    return cci
