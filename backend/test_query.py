import requests
import json

def test_db_status():
    url = 'http://localhost:5001/api/db-status'
    response = requests.get(url)
    print("Testing database status endpoint...")
    print("Response:", response.json())

def test_query(query):
    url = 'http://localhost:5001/api/query'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'query': query})
    response = requests.post(url, headers=headers, data=payload)
    print(f"Testing query: {query}")
    print("Response:", response.json())

if __name__ == '__main__':
    test_db_status()
    queries = [
        'top_sales_products',
        'total_sales_last_week',  # Example queries; adjust as needed
        'sales for Product X',
        'current stock for Product Y',
        'products with low stock',
        'details for Product Z',
        'list of products'
    ]
    for query in queries:
        test_query(query)
