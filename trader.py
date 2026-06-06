import config
import ntplib
import time

def get_client():
    from analyzer import patch_time
    patch_time()
    from pybit.unified_trading import HTTP
    return HTTP(
        testnet=config.BYBIT_TESTNET,
        api_key=config.BYBIT_API_KEY,
        api_secret=config.BYBIT_API_SECRET,
        recv_window=config.RECV_WINDOW,
    )

def get_balance(client):
    try:
        resp = client.get_wallet_balance(accountType="UNIFIED")
        for coin in resp["result"]["list"][0]["coin"]:
            if coin["coin"] == "USDT":
                return float(coin["walletBalance"])
    except Exception as e:
        print(f"Баланс қатесі: {e}")
    return 100

def set_leverage(client, symbol, leverage):
    try:
        client.set_leverage(
            category="linear",
            symbol=symbol,
            buyLeverage=str(leverage),
            sellLeverage=str(leverage)
        )
    except Exception:
        pass

def open_trade(client, symbol, direction, position):
    try:
        order_side = "Buy" if direction == "LONG" else "Sell"
        order = client.place_order(
            category="linear",
            symbol=symbol,
            side=order_side,
            orderType="Market",
            qty=str(position['qty']),
            stopLoss=str(position['sl_price']),
            takeProfit=str(position['tp_price']),
            timeInForce="GTC",
        )
        return order
    except Exception as e:
        print(f"Сделка қатесі: {e}")
        return None

def get_klines(client, symbol, interval, limit=200):
    response = client.get_kline(
        category="linear",
        symbol=symbol,
        interval=interval,
        limit=limit
    )
    import pandas as pd
    data = response['result']['list']
    df = pd.DataFrame(data, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume', 'turnover'
    ])
    df = df.astype(float)
    df = df.iloc[::-1].reset_index(drop=True)
    return df