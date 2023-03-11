from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import schemas,models

app = FastAPI()



#this code is for query to database
def get_db():
    db = SessionLocal()
    try:
      yield db
    finally:
      db.close()
      


#all posts list
@app.get("/api/v1/posts")
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.id.desc()).all()
    return {"message": "success" , 'data' : posts}



#single post
@app.get("/api/v1/posts/{id}")
def post(id , db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"message": "success" , 'data' : post}



#create post
@app.post("/api/v1/posts")
def create(request:schemas.PostBase , db:Session = Depends(get_db)):
    #validation with schemas.postbase
    post = models.Post(title = request.title , text = request.text)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "success" , 'data' : post}



#update post
@app.put("/api/v1/posts/{id}")
def update(id , request:schemas.PostBase, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).update({
        "title" : request.title,
        "text" : request.text
    })
    db.commit()
    return {"message": "success" , 'data' : post}



#delete post
@app.delete("/api/v1/posts/{id}")
def delete(id , db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    db.delete(post)
    db.commit()
    return {"message": "success"}
