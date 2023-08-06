import pandas as pd
import numpy as np
from binance.client import Client
from binance.enums import HistoricalKlinesType
from ta.volatility import average_true_range


def download_data(ticket: str, ts_start: int, ts_end: int = 0,
                  timeframe: str = Client.KLINE_INTERVAL_1MINUTE) -> pd.DataFrame:
    """ Скачать данные с Binance API """
    client = Client('', '')
    titles = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'Quote asset volume',
              'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored']
    data_generator = client.get_historical_klines_generator(
        symbol=ticket,
        interval=timeframe,
        start_str=ts_start * 1000,
        end_str=None if ts_end == 0 else ts_end * 1000,
        klines_type=HistoricalKlinesType.FUTURES
    )
    rows = []
    for row in data_generator:
        rows.append(row)
    df = pd.DataFrame(rows, columns=titles)
    df = df[['close_time', 'close', 'high', 'low', 'volume']]
    df[['close', 'high', 'low', 'volume']] = df[['close', 'high', 'low', 'volume']].astype(np.float64)
    return df


def calc_rel_atr(df: pd.DataFrame, atr_window: int) -> pd.Series:
    """ Расчитать относительный АТР """
    return average_true_range(df['high'], df['low'], df['close'], window=atr_window) / df['close'] * 100


def cal_rel_atr_by_other_timeframe(df: pd.DataFrame, ticket: str, atr_window: int,
                                   timeframe: str = Client.KLINE_INTERVAL_1DAY) -> pd.Series:
    """ Получить дневной атр """
    period_seconds = {
        Client.KLINE_INTERVAL_1DAY: 24 * 60 * 60,
        Client.KLINE_INTERVAL_4HOUR: 4 * 60 * 60,
        Client.KLINE_INTERVAL_1HOUR: 1 * 60 * 60,
        Client.KLINE_INTERVAL_30MINUTE: 30 * 60,
        Client.KLINE_INTERVAL_15MINUTE: 15 * 60
    }[timeframe]
    df_start_date = int(df['close_time'][0] / 1000)
    df_end_date = int(df['close_time'][len(df) - 1] / 1000)
    data = download_data(ticket, df_start_date - (atr_window + 1) * period_seconds, df_end_date, timeframe)
    data['atr'] = calc_rel_atr(data, atr_window)
    atr_by_days = {int(row['close_time']): row['atr'] for i, row in data.iterrows()}
    del data
    atr_arr = []
    for i, row in df.iterrows():
        for ts, atr in atr_by_days.copy().items():
            diff = (row['close_time'] - ts) / 1000
            if diff > period_seconds:
                del atr_by_days[ts]
            else:
                atr_arr.append(atr)
                break
    return pd.Series(atr_arr)