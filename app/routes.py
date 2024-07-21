from app import app
from flask import render_template
import mysql.connector
from mysql.connector import Error

# Define the database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'c0nygre',
    'database': 'mydatabase'
}

def get_db_connection():
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    return connection

# Define the home route
@app.route('/')
def home():
    connection = get_db_connection()
    if connection is None:
        return 'Failed to connect to the database', 500

    cursor = connection.cursor(dictionary=True)

    # stock info query
    cursor.execute("select stock_name, stock_symbol, market_name, country from stocks natural join markets")
    stocks = cursor.fetchall()

    # stock price query
    cursor.execute("select stock_name, stock_symbol, price, price_date from stocks natural"
                   " join stock_prices where price_date = '2024-07-02'")
    prices = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('home.html', stocks=stocks, prices=prices)

