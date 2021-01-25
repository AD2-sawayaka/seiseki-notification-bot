import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print("hello world")

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


conn = get_connection()
cur = conn.cursor()
cur.execute('SELECT * FROM actor')
for row in cur:
    print(row)
cur.close()
conn.close()
