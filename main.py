from fastapi import FastAPI
from fastapi import FastAPI,Response,status,HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel


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

class Post(BaseModel):
    house_number: int
    rent: int
    phone: str
    place: str


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO house (house_number,rent,phone,place) VALUES (%s,%s,%s,%s) RETURNING * """, (post.house_number,post.rent,post.phone,post.place))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post}