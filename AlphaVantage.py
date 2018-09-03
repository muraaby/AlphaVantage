import requests
import pandas as pd


class AlphaVantage:

    time_interval = '1min'
    out_put_size = 'full'
    data_type = 'pandas'
    api_key = None
    historical_interval = 'daily'

    def __init__(self):
        self.ticker = None

    def initiate(self, ticker):
        """
        :param ticker: example 'AAPL' or 'GOOGL'
        :return: assigns the ticker
        """
        self.ticker = ticker

    def quote(self, data_type=None):
        """
        :param data_type: one of the following ['list', 'json', 'csv', 'pandas'] *class default 'pandas'
        :return: most recent ticker data
        """
        if data_type is None:
            data_type = AlphaVantage.data_type
        elif data_type not in ['json', 'csv', 'list', 'pandas']:
            raise Exception('data type must be json, csv, list, or pandas')
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+self.ticker+'&apikey='+AlphaVantage.api_key+'&datatype='+data_type
        response = requests.get(url)
        if data_type is 'csv':
            return response.content
        elif data_type is 'json':
            return response.json()
        elif data_type in ['list', 'pandas']:
            df = response.json()['Global Quote']
            d_hold = list([['symbol', 'open', 'high', 'low', 'price', 'volume', 'latest trading day', 'previous close', 'change', 'change percent']])
            d_hold.append([(df[x]) for x in df])
            if data_type is 'list':
                return d_hold
            else:
                df = pd.DataFrame(d_hold[1:], columns=d_hold[0])
                df.set_index('symbol', inplace=True)
                return df

    def today(self, time_interval=None, out_put_size=None, data_type=None):
        """
        :param time_interval: ['1min', '5min', '15min', '30min', '60min', None] class default is '1min'
        :param out_put_size: ['full', 'compact', None]                          class default 'full *compact is limited to 100*
        :param data_type ['list', 'json', 'csv', 'pandas']                      class default 'pandas'
        :return: ticker data for today
        """
        if time_interval is None and AlphaVantage.time_interval in ['1min', '5min', '15min', '30min', '60min']:
            time_interval = AlphaVantage.time_interval
        elif time_interval is None and AlphaVantage.time_interval not in ['1min', '5min', '15min', '30min', '60min']:
            raise Exception('AlphaVantage.time_interval must be 1min, 5min, 15min, 30min, or 60min')
        elif time_interval not in ['1min', '5min', '15min', '30min', '60min']:
            raise Exception('time_interval must be 1min, 5min, 15min, 30min, or 60min')
        if out_put_size is None and AlphaVantage.out_put_size in ['full', 'compact']:
            out_put_size = AlphaVantage.out_put_size
        elif out_put_size is None and AlphaVantage.out_put_size not in ['full', 'compact']:
            raise Exception('AlphaVantage.out_put_size must be full or compact')
        elif out_put_size not in ['full', 'compact']:
            raise Exception('Out_put_size must either be full or compact')
        if data_type is None:
            if AlphaVantage.data_type in ['csv', 'json']:
                data_type = AlphaVantage.data_type
                data = data_type
            elif AlphaVantage.data_type in ['pandas', 'List']:
                data_type = 'json'
                data = AlphaVantage.data_type
            else:
                raise Exception('Data type must be pandas, list, json or csv')
        elif data_type in ['json', 'list', 'pandas']:
            data = data_type
            data_type = 'json'
        elif data_type is 'csv':
            data = data_type
        else:
            raise Exception('Data type must be list json pandas or csv')

        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'+'&symbol='+self.ticker+'&interval='+time_interval+'&outputsize='+out_put_size+'&apikey='\
              + AlphaVantage.api_key+'&datatype='+data_type

        response = requests.get(url)
        if data is 'csv':
            return response.content
        if data in ['json', 'list', 'pandas']:
            df = response.json()
            if data is 'json':
                return df
            elif data in ['list', 'pandas']:
                df = df['Time Series (' + time_interval + ')']
                df_holder = list([['timestamp', 'open', 'high', 'low', 'close', 'volume']])
                for x in df:
                    d_hold = list([x])
                    for y in df[x]:
                        d_hold.append(df[x][y])
                    df_holder.append(d_hold)
                df = df_holder
                if data is 'list':
                    return df
                else:
                    df = pd.DataFrame(df[1:], columns=df[0])
                    df.set_index('timestamp', inplace=True)
                    return df

    def historical(self, historical_interval=None, adjusted=None, out_put_size=None, data_type=None):
        """
        :param historical_interval: ['daily', 'weekly', 'monthly'] no Default setting
        :param out_put_size: ['full', 'compact'] Default full
        :param adjusted [True, None] Default None
        :param data_type: ['json', 'csv', 'pandas', 'list'] Default Pandas
        :return: ticker data in specified time frame and format
        """
        intervals = {'daily': 'TIME_SERIES_DAILY', 'weekly': 'TIME_SERIES_WEEKLY', 'monthly': 'TIME_SERIES_MONTHLY'}
        if historical_interval is None and AlphaVantage.historical_interval not in ['daily', 'weekly', 'monthly']:
            raise Exception('historical interval must be daily weekly or monthly')
        elif historical_interval is None and AlphaVantage.historical_interval in ['daily', 'weekly', 'monthly']:
            interval = intervals[AlphaVantage.historical_interval]
        elif historical_interval not in ['daily', 'weekly', 'monthly']:
            raise Exception('time_interval must be daily weekly or monthly')
        else:
            interval = intervals[historical_interval]
        if adjusted is not None:
            adjusted = '_ADJUSTED'
        else:
            adjusted = ''
        if out_put_size is None and AlphaVantage.out_put_size in ['full', 'compact']:
            out_put_size = AlphaVantage.out_put_size
        elif out_put_size is None and AlphaVantage.out_put_size not in ['full', 'compact']:
            raise Exception('AlphaVantage.out_put_size must be full or compact')
        elif out_put_size not in ['full', 'compact']:
            raise Exception('Out_put_size must either be full or compact')
        if data_type is None:
            if AlphaVantage.data_type in ['csv', 'json']:
                data_type = AlphaVantage.data_type
                data = data_type
            elif AlphaVantage.data_type in ['pandas', 'List']:
                data_type = 'json'
                data = AlphaVantage.data_type
            else:
                raise Exception('Data type must be pandas, list, json or csv')
        elif data_type in ['json', 'list', 'pandas']:
            data = data_type
            data_type = 'json'
        elif data_type is 'csv':
            data = data_type
        else:
            raise Exception('Data type must be list json pandas or csv')

        url = 'https://www.alphavantage.co/query?function='+interval+adjusted+'&symbol='+self.ticker+'&outputsize='+out_put_size+'&apikey='\
              + AlphaVantage.api_key+'&datatype='+data_type

        series = {'daily': 'Time Series (Daily)', 'weekly': 'Weekly Time Series', 'monthly': 'Monthly Time Series'}
        response = requests.get(url)
        if data is 'csv':
            return response.content
        if data in ['json', 'list', 'pandas']:
            df = response.json()
            if data is 'json':
                return df
            elif data in ['list', 'pandas']:
                if adjusted is '':
                    headers = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
                else:
                    headers = ['timestamp', 'open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount', 'split coefficient']
                if historical_interval is None:
                    df = df[series[AlphaVantage.historical_interval]]
                else:
                    df = df[series[historical_interval]]
                df_holder = list([headers])
                for x in df:
                    d_hold = list([x])
                    for y in df[x]:
                        d_hold.append(df[x][y])
                    df_holder.append(d_hold)
                df = df_holder
                if data is 'list':
                    return df
                else:
                    df = pd.DataFrame(df[1:], columns=df[0])
                    df.set_index('timestamp', inplace=True)
                    return df