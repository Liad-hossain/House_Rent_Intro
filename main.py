from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()


try:
    conn=psycopg2.connect(host='localhost',database='House-Rent',user='postgres',password='password123',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ",error)


@app.get("/posts",status_code=status.HTTP_201_CREATED)
def get_posts(limit: int=5,place: str='%',rent: int=400000):
    cursor.execute("""SELECT * FROM house WHERE place like %s and rent<%s limit %s""",(place,rent,limit))
    posts=cursor.fetchall()
    return {"data": posts}