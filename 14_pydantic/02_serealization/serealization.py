from pydantic import BaseModel,ConfigDict
from typing import List
from datetime import datetime

class Address(BaseModel):
    street:str
    city:str
    zip_code:str
    
class User(BaseModel):
    id:int
    name:str
    email:str
    is_active:bool = True
    created_at:datetime
    address:Address
    tags:List[str] = []
    
    model_config = ConfigDict(
        json_encoders={datetime:lambda v: v.strftime('%d-%m-%Y $H:%M:%S')}
    )    
    
    
user = User(
    id=1,
    name="yash",
    email="test@test.com",
    created_at=datetime(2026,10,1,15,30),
    address=Address(
        street="Something 123",
        city="Noida",
        zip_code="123456",
    ),
    is_active=False,
    tags=["Premium","Subscriber"]
)

python_dict = user.model_dump()
print(user)
print("*" *30)
print("*" *30)
print(python_dict)

json_str = user.model_dump_json()

print("*" *30)
print("*" *30)
print(json_str)