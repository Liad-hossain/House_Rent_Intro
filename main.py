from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor


try:
    conn = psycopg2.connect(host='localhost',database='House-Rent',user='postgres',password='password123',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connection was successful!!")
except Exception as error:
    print("Connecting to Database failed")
    print("Error :",error)

app=FastAPI()

@app.get('/')
def root():
    return "Want a room in house for rent!!"

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM house """)
    posts=cursor.fetchall()
    return {"data":posts}