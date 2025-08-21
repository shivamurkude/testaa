from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, schemas
from database import engine, SessionLocal

# ✅ Create tables in DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog")

def create_blog(Blog: schemas.Blog, db: Session = Depends(get_db)):
    #calling the schema data and then putting inside the models table ,after putting in table .
#taking whole data of table in new schema called new_blog and putting it into db 
    # ✅ new_blog is new schema
    new_blog=models.Blog(title=Blog.title,body=Blog.body)
    #adding newschema we created 
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs
    