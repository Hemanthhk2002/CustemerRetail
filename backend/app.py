from flask import Flask, request, jsonify
import mysql.connector
from nlp_utils import extract_query_details, extract_product_name
import config

app = Flask(__name__)

# Configure MySQL
db_config = {
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'host': config.DB_HOST,
    'database': config.DB_NAME
}

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query')

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Extract details from the query
    query_type = extract_query_details(query)
    response = "Sorry, I didn't understand that query."

    # Handle different query types
    if query_type == 'top_sales_products':
        cursor.execute("""
            SELECT product_name, SUM(sales_amount) as total_sales
            FROM sales
            GROUP BY product_name
            ORDER BY total_sales DESC
            LIMIT 5
        """)
        results = cursor.fetchall()
        response = "Top 5 sales products:\n" + "\n".join([f"{r['product_name']}: {r['total_sales']}" for r in results])
    elif query_type == 'total_sales_last_week':
        cursor.execute("""
            SELECT SUM(sales_amount) as total_sales
            FROM sales
            WHERE sales_date BETWEEN NOW() - INTERVAL 1 WEEK AND NOW()
        """)
        result = cursor.fetchone()
        response = f"Total sales last week: {result['total_sales']}"
    elif query_type == 'product_sales':
        product_name = extract_product_name(query)
        cursor.execute("""
            SELECT SUM(sales_amount) as total_sales
            FROM sales
            WHERE product_name = %s AND sales_date BETWEEN NOW() - INTERVAL 1 MONTH AND NOW()
        """, (product_name,))
        result = cursor.fetchone()
        response = f"Total sales for {product_name} last month: {result['total_sales']}"
    elif query_type == 'current_stock':
        product_name = extract_product_name(query)
        cursor.execute("""
            SELECT stock_quantity
            FROM inventory
            WHERE product_name = %s
        """, (product_name,))
        result = cursor.fetchone()
        response = f"Current stock for {product_name}: {result['stock_quantity']}"
    elif query_type == 'low_stock_products':
        cursor.execute("""
            SELECT product_name, stock_quantity
            FROM inventory
            WHERE stock_quantity < 10
        """)
        results = cursor.fetchall()
        response = "Low stock products:\n" + "\n".join([f"{r['product_name']}: {r['stock_quantity']}" for r in results])
    elif query_type == 'product_details':
        product_name = extract_product_name(query)
        cursor.execute("""
            SELECT product_name, product_description
            FROM products
            WHERE product_name = %s
        """, (product_name,))
        result = cursor.fetchone()
        response = f"Details for {product_name}: {result['product_description']}"
    elif query_type == 'list_products':
        cursor.execute("""
            SELECT product_name
            FROM products
        """)
        results = cursor.fetchall()
        response = "Products available:\n" + "\n".join([r['product_name'] for r in results])

    cursor.close()
    conn.close()

    return jsonify({'response': response})

@app.route('/api/db-status', methods=['GET'])
def db_status():
    try:
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return jsonify({'status': 'success', 'message': 'Database connection is successful.'})
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': f'Error connecting to database: {err}'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
