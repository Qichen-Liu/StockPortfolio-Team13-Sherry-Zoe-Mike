from app import app
from flask import render_template, request, jsonify
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


def execute_query(query, params=None):
    """Execute a query."""
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


# Define the home route
@app.route('/')
def home():
    return render_template('home.html')


# Define the portfolio route
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    query = """
    select p.user_name, p.email, p.balance, p.total_value, s.symbol, s.stock_name, ps.quantity, s.price
    from portfolio p join portfolio_stocks ps on p.id = ps.portfolio_id
    join stocks s on ps.stock_id = s.id
    where p.id = 1
    """
    # Execute the query to obtain the result
    result = execute_query(query)
    balance = result[0]['balance'] if result else 0
    total_value = result[0]['total_value'] if result else 0
    user_name = result[0]['user_name'] if result else ''
    email = result[0]['email'] if result else ''
    return render_template('portfolio.html', user_name=user_name, email=email,
                           balance=balance, total_value=total_value, stocks=result)


# Define the buy stock route
# url = /api/portfolio/<portfolio_id>/buy?stock_id=<stock_id>&quantity=<quantity>
@app.route('/api/portfolio/<int:portfolio_id>/buy', methods=['POST'])
def buy_stock(portfolio_id):
    data = request.args
    stock_id = data.get('stock_id')
    quantity = data.get('quantity')

    try:
        # Update the transaction table
        transaction_query = """
        INSERT INTO transactions (portfolio_id, stock_id, transaction_type, quantity) VALUES (%s, %s, 'buy', %s)
        """, (portfolio_id, stock_id, quantity)
        execute_query(transaction_query)

        # Get the stock price
        stock_query = """
        select price from stocks where id = %s
        """, stock_id
        stock_info = execute_query(stock_query)

        # Update the portfolio_stock table
        portfolio_stock_query = """
        INSERT INTO portfolio_stocks (stock_name, portfolio_id, stock_id, quantity) VALUES (%s, %s, %s, %s)
        on duplicate key update quantity = quantity + values(quantity)
        """, (stock_info[0]['price'], portfolio_id, stock_id, quantity)
        execute_query(portfolio_stock_query)

        # Update the portfolio table
        portfolio_query = """
        update portfolio set balance = balance - %s, total_value = total_value + %s where id = %s
        """, (quantity * stock_info[0]['price'], quantity * stock_info[0]['price'], portfolio_id)
        execute_query(portfolio_query)

        return jsonify({'message': 'Stock bought successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Define the sell stock route
# url = /api/portfolio/<portfolio_id>/sell?stock_id=<stock_id>&quantity=<quantity>
@app.route('/api/portfolio/<int:portfolio_id>/sell', methods=['POST'])
def sell_stock(portfolio_id):
    data = request.args
    stock_id = data.get('stock_id')
    quantity = data.get('quantity')

    try:
        # Update the transaction table
        transection_query = """
        INSERT INTO transactions (portfolio_id, stock_id, transaction_type, quantity) VALUES (%s, %s, 'sell', %s)
        """, (portfolio_id, stock_id, quantity)
        execute_query(transection_query)

        # Get the stock price
        stock_query = """
        select price from stocks where id = %s
        """, stock_id
        stock_info = execute_query(stock_query)

        # Update the portfolio_stock table
        portfolio_stock_query = """
        INSERT INTO portfolio_stocks (stock_name, portfolio_id, stock_id, quantity) VALUES (%s, %s, %s, %s)
        on duplicate key update quantity = quantity - values(quantity)
        """, (stock_info[0]['price'], portfolio_id, stock_id, quantity)
        execute_query(portfolio_stock_query)

        # Update the portfolio table
        portfolio_query = """
        update portfolio set balance = balance + %s, total_value = total_value - %s where id = %s
        """, (quantity * stock_info[0]['price'], quantity * stock_info[0]['price'], portfolio_id)
        execute_query(portfolio_query)

        return jsonify({'message': 'Stock sold successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
