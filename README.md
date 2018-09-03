# AlphaVantage
##make sure pandas is installed##

This is a python Wrapper for the Alpha Vantage api:

So far the wrapper can call last trade data, intradaily data, and historical data for a ticker.

I have yet to add currancies and technical indicators (will add if there is interest)

How to use:

AlphaVantage.api_key = 'Your Api Key'
instance = AlphaVantage()
instance.initiate(ticker) #example 'GOOGL'

LAST TRADE DATA
instance.quote(data_type=None) #default data type is pandas however one can choose from 'list' 'json' 'csv' 'pandas'

INTRADAILY DATA
instance.today(time_interal=None, out_put_size=None, data_type=None)

time_interval default is '1min' options are by 1min, 5min, 15min, 30min, or 60min
out_put_size default is 'full' options are 'full' or 'compact' last 100
data_type same as above

HISTORICAL DATA
instance.historical(historical_interval=None, adjusted=None, out_put_size=None, data_type=None)

historical_interval has no defualt options are 'daily' 'weekly' or 'monthly'
adjusted is default 'None' options are 'None' or 'True'
out_put_size and data_type is same as above
