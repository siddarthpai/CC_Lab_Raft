import mysql.connector

connections = [
    {"name": "connection", "host": "localhost", "port": 3009, "user": "root", "password": "some_pass"},
    {"name": "connection1", "host": "localhost", "port": 3014, "user": "root", "password": "some_pass"},
    {"name": "connection2", "host": "localhost", "port": 3015, "user": "root", "password": "some_pass"},
    {"name": "connection3", "host": "localhost", "port": 3016, "user": "root", "password": "some_pass"},
    {"name": "connection4", "host": "localhost", "port": 3017, "user": "root", "password": "some_pass"},
    {"name": "connection5", "host": "localhost", "port": 3018, "user": "root", "password": "some_pass"}
]


try:
    for conn_info in connections:
        connection = mysql.connector.connect(
            host=conn_info["host"],
            port=conn_info["port"],
            user=conn_info["user"],
            password=conn_info["password"]
        )

        if connection.is_connected():  
            print(f"Connected to MySQL ({conn_info['name']})")
            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS cc_proj")

            cursor.execute("USE cc_proj")

            cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")

            print(f"Table 'students' created successfully in connection {conn_info['name']}")

            cursor.close()
            connection.close()
            print(f"Connection {conn_info['name']} closed\n")

except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")
