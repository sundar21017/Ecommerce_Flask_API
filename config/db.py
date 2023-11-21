import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3306,
    'database': 'qaSquareNowMfi',
    'raise_on_warnings': True,
}

db = mysql.connector.connect(**config)

if (db.is_connected()):
    print("Database Connected")
else:
    print("Database Not connected")