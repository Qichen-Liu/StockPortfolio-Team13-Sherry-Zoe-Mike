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