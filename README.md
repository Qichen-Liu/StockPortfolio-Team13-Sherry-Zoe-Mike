# Neueda Project

This project is a simple project that demonstrates the use of Restful API. The project is written in Python and uses the Flask framework.

# Team 13 Members
- Sherry Lu
- Zoe Xiao
- Mike Liu

# Project Structure

```
./
├── .venv/
├── app/
│   ├── static/
│   │   ├── scripts/
│   │   │   ├── linechart.js
│   │   │   └── piechart.js
│   │   └── images/
│   │       ├── mike.png
│   │       ├── sherry.png
│   │       ├── user.jpg
│   │       └── zoe.png
│   ├── templates/
│   │   ├── home.html
│   │   ├── portfolio.html
│   │   ├── stock.html
│   │   └── trade.html
│   ├── helpers/
│   │   ├── realtimePrice.py
│   │   └── databaseHelper.py
│   ├── __init__.py
│   └── routes.py
├── MySQL/
│   ├── MySQL_Data/
│   └── MySQL_Tables/
├── requirements.txt
└── run.py
```
![Blank diagram](https://github.com/user-attachments/assets/ff80f75c-b52d-4bea-a58a-dec72e3caeda)

# Run Project
```
pip install -r requirements.txt   // install required packages
python run.py                     // run program

```
# Database Design

### `stocks` Table
This table stores information about individual stocks.

- **`id`**: Integer, auto-incremented primary key.
- **`symbol`**: Varchar(10), unique, not null. The stock's ticker symbol.
- **`stock_name`**: Varchar(100), not null. The full name of the stock.

### `portfolio` Table
This table maintains user portfolios.

- **`id`**: Integer, auto-incremented primary key.
- **`user_name`**: Varchar(100), not null. The name of the user owning the portfolio.
- **`email`**: Varchar(100), not null. The user's email address.
- **`balance`**: Decimal(15, 2), not null. The current balance of the portfolio.
- **`total_value`**: Decimal(15, 2), not null. The total value of the portfolio's stocks.

### `portfolio_stocks` Table
This table links stocks to specific portfolios, tracking the quantity of each stock in a portfolio.

- **`id`**: Integer, auto-incremented primary key.
- **`stock_name`**: Varchar(100), not null. The name of the stock (used for reference).
- **`symbol`**: Varchar(10), unique, not null. The stock's ticker symbol.
- **`portfolio_id`**: Integer, foreign key referencing `portfolio(id)`.
- **`stock_id`**: Integer, foreign key referencing `stocks(id)`.
- **`quantity`**: Integer. The amount of the stock held in the portfolio.
- **`cost`**: Decimal(15, 2). The total cost of a kind of stocks.
- **Unique**: `(portfolio_id, stock_id)` ensures that a stock can only appear once per portfolio.

### `transactions` Table
This table records transactions (buy/sell actions) related to stocks within portfolios.

- **`id`**: Integer, auto-incremented primary key.
- **`portfolio_id`**: Integer, foreign key referencing `portfolio(id)`.
- **`stock_id`**: Integer, foreign key referencing `stocks(id)`.
- **`symbol`**: Varchar(10), not null. The stock's ticker symbol.
- **`transaction_type`**: Enum('buy', 'sell'). Indicates the type of transaction.
- **`price`**: Decimal(15, 2), not null. The price per stock unit during the transaction.
- **`quantity`**: Integer. The number of stock units involved in the transaction.
- **`transaction_date`**: Timestamp, defaulting to the current timestamp. The date and time of the transaction.

# API Functions

### Home Route
- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: Renders the home page (`home.html`).

### Get Portfolio
- **Endpoint**: `/api/portfolio`
- **Method**: `GET`
- **Description**: Retrieves and displays the portfolio details for a hardcoded portfolio ID (1). Includes user information, portfolio balance, total value, and stock holdings with their recent 30-day price history. Also provides a list of stocks available for purchase.

### Buy Stock
- **Endpoint**: `/api/portfolio/<portfolio_id>/buy`
- **Method**: `POST`
- **Description**: Processes a stock purchase request. Validates sufficient balance, records the transaction, updates the portfolio's stock holdings, and adjusts the portfolio balance. Redirects to the buy status page with success or error messages.

### Sell Stock
- **Endpoint**: `/api/portfolio/<portfolio_id>/sell`
- **Method**: `POST`
- **Description**: Processes a stock sale request. Checks if there is enough stock to sell, records the transaction, updates the portfolio's stock holdings, and adjusts the portfolio balance. Removes the stock entry if its quantity drops to zero. Redirects to the sell status page with success or error messages.

### Search Stock
- **Endpoint**: `/api/fetch-stock`
- **Method**: `GET`
- **Description**: Retrieves detailed information about a stock by its ID. Includes stock name, symbol, historical prices for the last 30 days, and current stock data. Also shows the quantity of the stock currently held in the portfolio.

### Update Balance
- **Endpoint**: `/api/adjust-balance`
- **Method**: `PUT`
- **Description**: Updates the portfolio balance. Used for testing purposes.

# Realtime Stock Price Helper Functions

### `get_last_30_days_stock_prices`
- **Description**: Retrieves historical stock prices for the past 30 days.
- **Parameters**: 
  - `symbol` (str): The ticker symbol of the stock.
- **Returns**: A list of tuples containing dates and adjusted closing prices for the past 30 days.

### `get_current_stock_price`
- **Description**: Retrieves the most recent stock price.
- **Parameters**: 
  - `symbol` (str): The ticker symbol of the stock.
- **Returns**: The adjusted closing price of the stock on the most recent date.

### `get_stock_data`
- **Description**: Retrieves the most recent stock data, including the price, high, low, and volume.
- **Parameters**: 
  - `symbol` (str): The ticker symbol of the stock.
- **Returns**: A dictionary containing the stock’s symbol, price, high, low, and volume on the most recent date.

