import mysql.connector

DB_CONFIG = {
    'host': 'database-4.c3wwio6c8bng.eu-north-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Janhvi123',
    'database': 'expenses_db',
    'port': 3306,
    'connect_timeout': 10
}

try:
    print("Connecting to RDS...")
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Connected successfully!")
    conn.close()
except mysql.connector.Error as e:
    print("❌ Error connecting:", e)
