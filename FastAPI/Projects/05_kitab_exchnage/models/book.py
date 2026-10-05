from sqlmodel import SQLModel, Field,Relationship
from typing import  Optional

class Book(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: int = Field(gt=0)
    is_sold: bool = Field(default=False)
    
    # Foreign key to the User table
    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")
    
# Request body for creating a new book
class BookCreate(SQLModel):
    title: str
    author: str
    price: int = Field(gt=0)   
    user_id: int
    
# Response body for returning book information
class BookRead(Book):
    id: int
    title: str
    author: str
    price: int
    is_sold: bool
    user_id: int
    
class BookUpdate(SQLModel):
    price: Optional[int] = None
    is_sold: Optional[bool] = None

from models.user import User
Book.model_rebuild()