# import requests
# from datetime import datetime, timedelta
#
# ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key'
# ALPHA_VANTAGE_URL = 'https://www.alphavantage.co/query'
#
# def get_last_30_days_stock_prices(symbol):
#     params = {
#         'function': 'TIME_SERIES_DAILY',
#         'symbol': symbol,
#         'apikey': ALPHA_VANTAGE_API_KEY
#     }
#     response = requests.get(ALPHA_VANTAGE_URL, params=params)
#     data = response.json()
#     try:
#         time_series = data['Time Series (Daily)']
#         last_30_days_prices = []
#         today = datetime.today()
#         for i in range(30):
#             date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
#             if date in time_series:
#                 price = float(time_series[date]['1. open'])
#                 last_30_days_prices.append((date, price))
#         return last_30_days_prices
#     except KeyError as e:
#         print(f"KeyError: {e}")
#         print(f"API Response: {data}")
#         return None
#     except Exception as e:
#         print(f"Exception: {e}")
#         return None
#
# print(get_last_30_days_prices('TSLA'))
#
#
# def get_current_stock_price(symbol):
#     params = {
#         'function': 'TIME_SERIES_DAILY',
#         'symbol': symbol,
#         'apikey': ALPHA_VANTAGE_API_KEY
#     }
#     response = requests.get(ALPHA_VANTAGE_URL, params=params)
#     data = response.json()
#     try:
#         time_series = data['Time Series (Daily)']
#         most_recent_date = max(time_series.keys())
#         price = float(time_series[most_recent_date]['1. open'])
#         return price
#     except KeyError as e:
#         print(f"KeyError: {e}")
#         print(f"API Response: {data}")
#         return None
#     except Exception as e:
#         print(f"Exception: {e}")
#         return None
#
# print(get_current_price('TSLA'))


from datetime import datetime, timedelta
import pandas as pd

def get_last_30_days_stock_prices(symbol):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    # Convert dates to timestamps
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    df = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history&includeAdjustedClose=true",
    parse_dates = ['Date'], index_col='Date')
    # Select only the 'Adj Close' column and format as a list of tuples
    price_data = [(date.strftime('%Y-%m-%d'), float(row['Adj Close'])) for date, row in df.iterrows()][::-1]

    return price_data

def get_current_stock_price(symbol):
    df = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true",
    parse_dates = ['Date'], index_col='Date')
    most_recent_date = df.index[-1]
    price = float(df.loc[most_recent_date]['Adj Close'])

    return price
