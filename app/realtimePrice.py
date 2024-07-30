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


print(get_last_30_days_stock_prices('META'))