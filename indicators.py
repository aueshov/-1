import pandas as pd
import ta

def calculate_indicators(df):
    # EMA
    df['ema21'] = ta.trend.ema_indicator(df['close'], window=21)
    df['ema50'] = ta.trend.ema_indicator(df['close'], window=50)
    df['ema200'] = ta.trend.ema_indicator(df['close'], window=200)

    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)

    # MACD
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_hist'] = macd.macd_diff()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['close'], window=20)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_middle'] = bb.bollinger_mavg()
    df['bb_lower'] = bb.bollinger_lband()
    df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle'] * 100

    # ATR (Stop Loss үшін)
    df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)

    # Stochastic
    stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()

    # Volume анализі
    df['volume_sma'] = df['volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_sma']

    # Свеча паттерндері
    df['candle_body'] = abs(df['close'] - df['open'])
    df['candle_range'] = df['high'] - df['low']
    df['body_ratio'] = df['candle_body'] / df['candle_range']

    return df

def get_market_data(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3]

    return {
        'price': last['close'],
        'ema21': last['ema21'],
        'ema50': last['ema50'],
        'ema200': last['ema200'],
        'rsi': last['rsi'],
        'macd': last['macd'],
        'macd_signal': last['macd_signal'],
        'macd_hist': last['macd_hist'],
        'macd_hist_prev': prev['macd_hist'],
        'bb_upper': last['bb_upper'],
        'bb_lower': last['bb_lower'],
        'bb_middle': last['bb_middle'],
        'bb_width': last['bb_width'],
        'atr': last['atr'],
        'stoch_k': last['stoch_k'],
        'stoch_d': last['stoch_d'],
        'volume_ratio': last['volume_ratio'],
        'ema21_prev': prev['ema21'],
        'ema50_prev': prev['ema50'],
        'price_prev': prev['close'],
        'price_prev2': prev2['close'],
    }