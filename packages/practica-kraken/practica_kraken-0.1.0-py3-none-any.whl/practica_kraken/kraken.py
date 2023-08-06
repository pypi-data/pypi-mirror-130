from datetime import datetime
import time
import pandas as pd
import numpy as np
import math


class Kraken:

    @classmethod
    def get_asset_info(cls, k):
        assets = k.get_asset_info()
        return assets

    @classmethod
    def set_pair(cls, k, coin1, coin2):
        pairs_info = k.get_tradable_asset_pairs()
        pair = coin1 + coin2
        if pair not in pairs_info['altname']:
            print('No existe mercado para el par de monedas')
        else:
            return pair

    @classmethod
    def set_dates(cls, k, date, hours):
        date = date.split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        ini_min = None
        fin_min = None
        if type(hours[0]) == 'float':
            _, ini_hour = math.modf(hours[0])
            ini_min = 30
            if type(hours[1]) == 'float':
                _, fin_hour = math.modf(hours[1])
                fin_min = 30
            else:
                fin_hour = hours[1]
        elif type(hours[1]) == 'float':
            ini_hour = hours[0]
            _, fin_hour = math.modf(hours[1])
            fin_min = 30
        else:
            ini_hour = hours[0]
            fin_hour = hours[1]
        if fin_hour == 24:
            fin_hour = 23
            fin_min = 59
        ini_hour = int(ini_hour)
        fin_hour = int(fin_hour)
        if ini_min is not None:
            from_time = datetime(year, month, day, ini_hour, ini_min)
        else:
            from_time = datetime(year, month, day, ini_hour)
        if fin_min is not None:
            to_time = datetime(year, month, day, fin_hour, fin_min)
        else:
            to_time = datetime(year, month, day, fin_hour)
        unix_from_time = k.datetime_to_unixtime(from_time)
        unix_to_time = k.datetime_to_unixtime(to_time)
        return unix_from_time, unix_to_time

    @classmethod
    def get_recent_dates(cls, k, pair, from_date, to_date):
        df_trades = pd.DataFrame()
        i = 0
        while from_date < to_date:
            if i > 0:
                if i == 10:
                    i = 0
                    time.sleep(5)
                time.sleep(1)
            trades, last = k.get_recent_trades(pair, from_date)
            df_trades = df_trades.append(trades.reset_index(), ignore_index=True)
            from_date = int(last/1e9)
            i += 1
        df_trades = df_trades[df_trades['dtime'] <= k.unixtime_to_datetime(to_date)]
        df_trades.sort_values(by=['dtime'], ascending=True, inplace=True)
        return df_trades

    @classmethod
    def calculate_vwap(cls, prices, volumes):
        prices = np.array(prices)
        volumes = np.array(volumes)
        if len(prices) > 0:
            calculated_vwap = sum(prices * volumes) / sum(volumes)
            return calculated_vwap

    @classmethod
    def get_df_vwap(cls, df_trades, frecuency):
        if frecuency == '1 hora':
            frecuency = '1H'
        if frecuency == '4 horas':
            frecuency = '4H'
        if frecuency == '24 horas':
            frecuency = '24H'
        df_vwap = df_trades.groupby(pd.Grouper(key='dtime', freq=frecuency)).\
            apply(lambda x: cls.calculate_vwap(x['price'], x['volume'])).reset_index(name='vwap')
        return df_vwap
