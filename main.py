from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

class updatePost(BaseModel):
    house_number: int=-1
    rent: int=-1
    phone: str=""
    place: str=""


try:
    conn=psycopg2.connect(host='localhost',database='House-Rent',user='postgres',password='password123',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ",error)

@app.patch("/posts/{id}")
def update_post(id: int, post: updatePost):
    if post.house_number!=-1:
        cursor.execute("""UPDATE house SET house_number=%s WHERE id=%s RETURNING * """, (post.house_number,str(id)))
    if post.rent!=-1:
        cursor.execute("""UPDATE house SET rent=%s WHERE id=%s RETURNING * """, (post.rent,str(id)))
    if post.phone!="":
        cursor.execute("""UPDATE house SET phone=%s WHERE id=%s RETURNING * """, (post.phone,str(id)))
    if post.place!="":
        cursor.execute("""UPDATE house SET place=%s WHERE id=%s RETURNING * """, (post.place,str(id)))
    conn.commit()

    return "Updated Successfully"