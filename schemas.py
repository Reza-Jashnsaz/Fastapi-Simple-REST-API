from pydantic import BaseModel


#for validation
class PostBase(BaseModel):
    title : str
    text : str
    
class Post(PostBase):
    id : int
    class Config:
        orm_mode = True
    
    
#we can make more classes for create form or update