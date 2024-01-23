import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = connection.cursor()

db_name = "testdb"
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

cursor.close()
connection.close()
