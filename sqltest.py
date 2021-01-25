import psycopg2
import os
from dotenv import load_dotenv





load_dotenv()

print("hello world")

def isUpdate(name):
    query = "SELECT subject_name FROM seiseki WHERE subject_name = '" + name +  "'"
    #print(query)
    
    cur.execute(query)
    tmp = str()
    for row in cur:
        tmp = row
    if tmp:
        return False
    return True



def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


conn = get_connection()
cur = conn.cursor()
#cur.execute('SELECT * FROM actor')
#cur.execute()
print(isUpdate('論理回路'))

cur.close()
conn.close()
