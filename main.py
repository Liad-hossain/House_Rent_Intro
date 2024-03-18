from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

class Post(BaseModel):
    house_number: int
    rent: int
    phone: str
    place: str


try:
    conn=psycopg2.connect(host='localhost',database='House-Rent',user='postgres',password='password123',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ",error)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    cursor.execute("""UPDATE house SET house_number=%s,rent=%s,phone=%s,place=%s WHERE id=%s RETURNING * """, (post.house_number,post.rent,post.phone,post.place,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    return {"data": updated_post}