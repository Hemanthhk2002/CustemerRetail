import mysql.connector
from mysql.connector import Error

def connect_to_mysql():
    try:
        # Establish connection
        connection = mysql.connector.connect(
            host='127.0.0.1',    # MySQL server host (e.g., localhost or IP address)
            database='retail_db',  # Database name
            user='root',           # MySQL username
            password='hemanthK2002'        # MySQL password
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            
            # Create a cursor object
            cursor = connection.cursor()
            
            # Execute a SQL query
            query = "SELECT * FROM your_table_name"
            cursor.execute(query)
            
            # Fetch and print all the results
            result = cursor.fetchall()
            for row in result:
                print(row)
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        # Close the connection if open
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Call the function to connect to the database
connect_to_mysql()