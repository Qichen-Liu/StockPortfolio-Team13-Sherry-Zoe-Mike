from app import app
from flask import render_template, request, jsonify, redirect, url_for
from app.databaseHelper import execute_query
from app.realtimePrice import get_current_stock_price, get_last_30_days_stock_prices, get_stock_data


# Define the home route
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# Define the portfolio route
@app.route('/api/portfolio', methods=['GET'])
# TODO: Update the query to get the cost for each stock
def get_portfolio():
    query = """
    select p.user_name, p.email, p.balance, s.symbol, s.stock_name, ps.quantity, s.id, ps.cost
    from portfolio p join portfolio_stocks ps on p.id = ps.portfolio_id
    join stocks s on ps.stock_id = s.id
    where p.id = 1
    """
    # Execute the query to obtain the result
    result = execute_query(query)
    balance = result[0]['balance'] if result else 10000
    user_name = result[0]['user_name'] if result else 'Mike Liu'
    email = result[0]['email'] if result else 'random.rd@random.com'

    # Prepare stock data and current total value of the portfolio
    stock_hold = []
    total_value = 0.0

    for stock in result:
        last_30_days_prices = get_last_30_days_stock_prices(stock['symbol'])
        avg_cost_pershare = float(stock['cost']) / stock['quantity']
        stock_info = {
            'id': stock['id'],
            'stock_name': stock['stock_name'],
            'symbol': stock['symbol'],
            'quantity': stock['quantity'],
            'last_30_days_prices': last_30_days_prices,
            'percent_gain_loss': (last_30_days_prices[0][1] - avg_cost_pershare) / avg_cost_pershare * 100
        }
        stock_hold.append(stock_info)
        total_value += stock['quantity'] * last_30_days_prices[0][1]

    stock_query = """
    select id, stock_name, symbol from stocks
    """
    stocks_can_buy = execute_query(stock_query)

    transaction_query = """
    select t.transaction_type, t.price, t.quantity, s.stock_name, s.symbol from transactions t
    join stocks s on t.stock_id = s.id
    where t.portfolio_id = %s
    """
    transactions = execute_query(transaction_query, (1,))

    return render_template('portfolio.html', user_name=user_name, email=email,
                           balance=balance, total_value=total_value, stocks_can_sell=stock_hold,
                           stocks_can_buy=stocks_can_buy, transactions=transactions)
    #return jsonify({'stocks': stock_hold, 'user_name': user_name, 'email': email, 'balance': balance})


# Define the buy stock route
# url = /api/portfolio/<portfolio_id>/buy
# TODO: Update the cost of the stock in portfolio_stock table
@app.route('/api/portfolio/<int:portfolio_id>/buy', methods=['POST'])
def buy_stock(portfolio_id):
    data = request.form
    stock_id = data.get('stock_id')
    quantity = int(data.get('quantity'))

    print(f"buy stock_id: {stock_id}, quantity: {quantity}")

    try:
        # check if we have enough balance
        balance_query = """
        select balance from portfolio where id = %s
        """
        balance = execute_query(balance_query, (portfolio_id,))[0]['balance']

        # Get the stock info
        stock_query = """
                select stock_name, symbol from stocks where id = %s
                """
        stock_info = execute_query(stock_query, (stock_id,))
        stock_symbol = stock_info[0]['symbol']
        print(f"stock_symbol: {stock_symbol}")
        stock_price = get_current_stock_price(stock_symbol)
        print(f"stock_price: {stock_price}")

        stock_name = stock_info[0]['stock_name']
        # check balance is enough
        if balance < quantity * stock_price:
            return jsonify({'error': 'Not enough balance'}), 400

        # Update the transaction table
        transaction_query = """INSERT INTO transactions (portfolio_id, stock_id, symbol, transaction_type, price, quantity) 
        VALUES (%s, %s, %s, 'buy', %s, %s)"""

        execute_query(transaction_query, (portfolio_id, stock_id, stock_symbol, stock_price, quantity))

        # Update the portfolio_stock table with cost
        portfolio_stock_query = """
        INSERT INTO portfolio_stocks (stock_name, symbol, portfolio_id, stock_id, quantity, cost) VALUES 
        (%s, %s, %s, %s, %s, %s) on duplicate key 
        update quantity = quantity + values(quantity), cost = values(cost) + cost
        """
        execute_query(portfolio_stock_query,
                      (stock_name, stock_symbol, portfolio_id, stock_id, quantity, quantity * stock_price))

        # Update the portfolio table
        portfolio_query = """
        update portfolio set balance = balance - %s where id = %s
        """
        execute_query(portfolio_query, (quantity * stock_price, portfolio_id))

        return redirect(url_for('buy_status', status='success', message='Stock bought successfully'))

    except Exception as e:
        return redirect(url_for('buy_status', status='error', message=str(e)))


# Define the sell stock route
# url = /api/portfolio/<portfolio_id>/sell
# TODO: Update the cost of the stock in portfolio_stock table
# @app.route('/api/portfolio/<int:portfolio_id>/sell', methods=['POST'])
# def sell_stock(portfolio_id):
#     data = request.form
#     stock_id = data.get('stock_id')
#     sell_quantity = int(data.get('quantity'))
#
#     print(f"sell stock_id: {stock_id}, quantity: {sell_quantity}")
#     print()
#
#     try:
#
#         # check if we have enough stock to sell
#         portfolio_stocks_query = """
#         select quantity, symbol, cost from portfolio_stocks where portfolio_id = %s and stock_id = %s
#         """
#         stocks = execute_query(portfolio_stocks_query, (portfolio_id, stock_id))
#         stock_quantity = stocks[0]['quantity'] if stocks else 0
#         stock_symbol = stocks[0]['symbol'] if stocks else ''
#         stock_cost = stocks[0]['cost'] if stocks else 0
#
#
#         print()
#         print("stock_quantity holds: ", stock_quantity)
#         print("stock_symbol holds: ", stock_symbol)
#
#         if stock_quantity < sell_quantity:
#             return jsonify({'error': 'Not enough stock to sell'}), 400
#
#         # Get the stock price
#         stock_price = get_current_stock_price(stock_symbol)
#         print(f"stock_price: {stock_price}")
#
#         # Update the transaction table
#         transaction_query = """INSERT INTO transactions (portfolio_id, stock_id, symbol, transaction_type, price,
#         quantity) VALUES (%s, %s, %s, 'sell', %s, %s)"""
#
#         execute_query(transaction_query, (portfolio_id, stock_id, stock_symbol, stock_price, sell_quantity))
#
#         # Get the stock
#         stock_query = """
#                         select stock_name, symbol from stocks where id = %s
#                         """
#         stock_info = execute_query(stock_query, (stock_id,))
#         stock_symbol = stock_info[0]['symbol']
#         print(f"stock_symbol: {stock_symbol}")
#
#         stock_name = stock_info[0]['stock_name']
#         print(f"stock_name: {stock_name}")
#
#         #TODO: Update the portfolio_stock table, check the cost
#
#         # Calculate the cost per share and the cost of the shares being sold
#         cost_per_share = stock_cost / stock_quantity
#         cost_of_sold_shares = cost_per_share * sell_quantity
#         print(f"cost_per_share: {cost_per_share}, cost_of_sold_shares: {cost_of_sold_shares}")
#
#         portfolio_stock_query = """
#                 UPDATE portfolio_stocks SET quantity = quantity - %s, total_cost = total_cost - %s
#                 WHERE portfolio_id = %s AND stock_id = %s
#                 """
#         execute_query(portfolio_stock_query,
#                       (sell_quantity, cost_of_sold_shares, portfolio_id, stock_id))
#
#         # Remove the record if quantity becomes 0
#         delete_query = """
#                 DELETE FROM portfolio_stocks
#                 WHERE portfolio_id = %s AND stock_id = %s AND quantity <= 0
#                 """
#         execute_query(delete_query, (portfolio_id, stock_id))
#
#         # Update the portfolio table
#         portfolio_query = """
#                 update portfolio set balance = balance + %s where id = %s
#                 """
#         execute_query(portfolio_query, (sell_quantity * stock_price, portfolio_id))
#
#         return redirect(url_for('sell_status', status='success', message='Stock sold successfully'))
#
#     except Exception as e:
#         return redirect(url_for('sell_status', status='error', message=str(e)))


# Define the sell stock route
# url = /api/portfolio/<portfolio_id>/sell
@app.route('/api/portfolio/<int:portfolio_id>/sell', methods=['POST'])
def sell_stock(portfolio_id):
    data = request.form
    stock_id = data.get('stock_id')
    quantity = int(data.get('quantity'))

    print(f"sell stock_id: {stock_id}, quantity: {quantity}")

    try:

        # check if we have enough stock to sell
        portfolio_stocks_query = """
        select quantity, symbol from portfolio_stocks where portfolio_id = %s and stock_id = %s
        """
        stocks = execute_query(portfolio_stocks_query, (portfolio_id, stock_id))
        stock_quantity = stocks[0]['quantity'] if stocks else 0
        stock_symbol = stocks[0]['symbol'] if stocks else ''

        print(stocks)
        print("stock_quantity holds: ", stock_quantity)

        if stock_quantity < quantity:
            return jsonify({'error': 'Not enough stock to sell'}), 400

        # Get the stock price
        stock_price = get_current_stock_price(stock_symbol)
        print(f"stock_price: {stock_price}")

        # Update the transaction table
        transaction_query = """INSERT INTO transactions (portfolio_id, stock_id, symbol, transaction_type, price, quantity) 
                VALUES (%s, %s, %s, 'sell', %s, %s)"""

        execute_query(transaction_query, (portfolio_id, stock_id, stock_symbol, stock_price, quantity))

        # Get the stock
        stock_query = """
                        select stock_name, symbol from stocks where id = %s
                        """
        stock_info = execute_query(stock_query, (stock_id,))
        stock_symbol = stock_info[0]['symbol']
        print(f"stock_symbol: {stock_symbol}")
        stock_price = get_current_stock_price(stock_symbol)
        print(f"stock_price: {stock_price}")
        stock_name = stock_info[0]['stock_name']

        # Update the portfolio_stock table
        portfolio_stock_query = """
                INSERT INTO portfolio_stocks (stock_name, symbol, portfolio_id, stock_id, quantity) VALUES 
                (%s, %s, %s, %s, %s) on duplicate key update quantity = quantity - values(quantity)
                """
        execute_query(portfolio_stock_query, (stock_name, stock_symbol, portfolio_id, stock_id, quantity))

        # Remove the record if quantity becomes 0
        delete_query = """
                DELETE FROM portfolio_stocks
                WHERE portfolio_id = %s AND stock_id = %s AND quantity <= 0
                """
        execute_query(delete_query, (portfolio_id, stock_id))

        # Update the portfolio table
        portfolio_query = """
                update portfolio set balance = balance + %s where id = %s
                """
        execute_query(portfolio_query, (quantity * stock_price, portfolio_id))

        return redirect(url_for('sell_status', status='success', message='Stock sold successfully'))

    except Exception as e:
        return redirect(url_for('sell_status', status='error', message=str(e)))


# Define the buy status route
@app.route('/api/buy-status', methods=['GET'])
def buy_status():
    status = request.args.get('status', 'error')
    message = request.args.get('message', 'An unknown error occurred.')
    return render_template('buyStatus.html', status=status, message=message)


# Define the sell status route
@app.route('/api/sell-status', methods=['GET'])
def sell_status():
    status = request.args.get('status', 'error')
    message = request.args.get('message', 'An unknown error occurred.')
    return render_template('sellStatus.html', status=status, message=message)


# Define the search stock route
# sample url = /api/fetch-stock?id=1
@app.route('/api/fetch-stock', methods=['GET'])
def search_stock():
    stock_id = request.args.get('id')
    portfolio_id = 1
    stock_query = """
    select stock_name, symbol from stocks where id = %s
    """
    result = execute_query(stock_query, (stock_id,))
    symbol = result[0]['symbol'] if result else ''
    stock_name = result[0]['stock_name'] if result else ''
    historical_prices = get_last_30_days_stock_prices(symbol)
    stock_detail = get_stock_data(symbol)

    portfolio_stocks_query = """
           select quantity from portfolio_stocks where portfolio_id = %s and stock_id = %s
           """
    stocks = execute_query(portfolio_stocks_query, (portfolio_id, stock_id))
    stock_quantity = stocks[0]['quantity'] if stocks else 0

    return render_template('stock.html', stock_name=stock_name, symbol=symbol, stock_detail=stock_detail,
                           historical_prices=historical_prices, stock_id=stock_id, stock_quantity=stock_quantity)


# TODO: Define the route for trade page
@app.route('/api/trade', methods=['GET'])
def trade():
    return render_template('trade.html')
