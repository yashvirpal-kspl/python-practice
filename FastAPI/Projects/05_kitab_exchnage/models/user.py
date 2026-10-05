from sqlmodel import SQLModel, Field,Relationship
from typing import  Optional

#Database Table for User
class User(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    collage: str
    
    # One user can have many books
    books: list["Book"] = Relationship(back_populates="owner")


# Request body for creating a new user
class UserCreate(SQLModel):
    name: str
    email: str
    collage: str
    
# Response body
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    collage: str

# Avoid circular import

from models.book import Book
User.model_rebuild