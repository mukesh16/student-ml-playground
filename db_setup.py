import psycopg2
from psycopg2 import sql

# Database Configuration
DB_NAME = "tabtognn"
DB_USER = "demo"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# # Connect to PostgreSQL
# conn = psycopg2.connect(
#     dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
# )
# conn.autocommit = True
# cur = conn.cursor()

# # Create database if not exists
# cur.execute(sql.SQL(f"CREATE DATABASE {DB_NAME};"))

# # Close connection
# cur.close()
# conn.close()

# Connect to new database
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

# Create table for file uploads
cur.execute("""
    CREATE TABLE IF NOT EXISTS file_uploads (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

conn.commit()
cur.close()
conn.close()

print("Database and table created successfully!")