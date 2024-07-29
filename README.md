# Neueda Project

This project is a simple project that demonstrates the use of Restful API. The project is written in Python and uses the Flask framework.

# Team 13 Members
- Sherry Lu
- Zoe Xiao
- Mike Liu

# Project Structure

```
.
├── .venv/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── template/
│       ├── home.html
│       ├── portfolio.html
│       ├── buyStatus.html
│       └── sellStatus.html
├── run.py
├── MySQL/
│   ├── table.sql
│   └── data.sql
└── requirements.txt
```
![Blank diagram (2)](https://github.com/user-attachments/assets/f06a0ff0-c448-42f2-a274-8f1eb3286d25)

# Run Project
```
pip install -r requirements.txt   // install required packages
python run.py                     // run program

```
# Database Schema

### `stocks`
This table stores information about the stocks available for trading.

- `id`: An auto-incremented primary key for each stock.
- `symbol`: A unique stock symbol (e.g., AAPL for Apple Inc.), with a maximum length of 10 characters.
- `stock_name`: The name of the stock, with a maximum length of 100 characters.
- `price`: The current price of the stock, stored as a decimal value with two decimal places.

### `portfolio`
This table stores information about user portfolios.

- `id`: An auto-incremented primary key for each portfolio.
- `user_name`: The name of the portfolio owner, with a maximum length of 100 characters.
- `email`: The email address of the portfolio owner, with a maximum length of 100 characters.
- `balance`: The current balance of the portfolio, stored as a decimal value with two decimal places.
- `total_value`: The total value of the portfolio, stored as a decimal value with two decimal places.

### `portfolio_stocks`
This table links portfolios to the stocks they contain and stores the quantity of each stock in a portfolio.

- `id`: An auto-incremented primary key for each portfolio-stock relationship.
- `stock_name`: The name of the stock, with a maximum length of 100 characters.
- `portfolio_id`: A foreign key linking to the `portfolio` table.
- `stock_id`: A foreign key linking to the `stocks` table.
- `quantity`: The number of shares of the stock in the portfolio.
- `unique(portfolio_id, stock_id)`: Ensures that each portfolio can only have one entry for each stock.

### `transactions`
This table stores information about transactions (buying and selling stocks) within portfolios.

- `id`: An auto-incremented primary key for each transaction.
- `portfolio_id`: A foreign key linking to the `portfolio` table.
- `stock_id`: A foreign key linking to the `stocks` table.
- `transaction_type`: The type of transaction (`buy` or `sell`).
- `quantity`: The number of shares involved in the transaction.
- `transaction_date`: The date and time of the transaction, with a default value of the current timestamp.
