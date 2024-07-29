import requests
from datetime import datetime, timedelta

ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key'
ALPHA_VANTAGE_URL = 'https://www.alphavantage.co/query'

# Get the last 30 days prices for a stock
def get_last_30_days_prices(symbol):
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(ALPHA_VANTAGE_URL, params=params)
    data = response.json()
    try:
        time_series = data['Time Series (Daily)']
        last_30_days_prices = []
        today = datetime.today()
        for i in range(30):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if date in time_series:
                price = float(time_series[date]['1. open'])
                last_30_days_prices.append((date, price))
        return last_30_days_prices
    except KeyError:
        return None


# Get the current price for a stock
def get_current_price(symbol):
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(ALPHA_VANTAGE_URL, params=params)
    data = response.json()
    try:
        price = float(data['Global Quote']['05. price'])
        return price
    except KeyError:
        return None