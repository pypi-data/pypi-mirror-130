from binance import Client

ACCOUNT_CLIENT_PARAMS = {
    "KUCOIN": [
        "KUCOIN_API_KEY",
        "KUCOIN_API_SECRET",
        "KUCOIN_API_PASSPHRASE"
    ],
    "BINANCE": [
        "BINANCE_API_KEY",
        "BINANCE_API_SECRET"
    ]
}

KUCOIN_FRAME_CONV = {
    "1min":60, "3min":180, "5min":300, "15min":900, "30min":1800, "1hour":3600, "2hour":7200, "4hour": 14400, "6hour":21600, "8hour":28800, "12hour":43200, "1day":86400, "1week":604800
}


BINANCE_INTERVALS = {
    '1m': Client.KLINE_INTERVAL_1MINUTE,
    '3m': Client.KLINE_INTERVAL_3MINUTE,
    '5m': Client.KLINE_INTERVAL_5MINUTE,
    '15m': Client.KLINE_INTERVAL_15MINUTE,
    '30m': Client.KLINE_INTERVAL_30MINUTE,
    '1h': Client.KLINE_INTERVAL_1HOUR,
    '2h': Client.KLINE_INTERVAL_2HOUR,
    '4h': Client.KLINE_INTERVAL_4HOUR,
    '6h': Client.KLINE_INTERVAL_6HOUR,
    '8h': Client.KLINE_INTERVAL_8HOUR,
    '12h': Client.KLINE_INTERVAL_12HOUR,
    '1d': Client.KLINE_INTERVAL_1DAY,
    '3d': Client.KLINE_INTERVAL_3DAY,
    '1w': Client.KLINE_INTERVAL_1WEEK,
    '1M': Client.KLINE_INTERVAL_1MONTH,
}