from typing import List,Optional
from pydantic import BaseModel

class Address(BaseModel):
    street:str
    city:str
    postal_code:str
    
class User(BaseModel):
    id:int
    name:str
    address:Address
    

address = Address(
    street="123 Something",
    city="Noida",
    postal_code="123456"
) 

user = User(
    id=1,
    name="Yashvir",
    address= address
)       

user_data = {
    "id":1,
    "name":"Yashvir",
    "address":{
        "street":"321 Something",
        "city":"Kyoto",
        "postal_code":"121313"
    }
}

user = User(**user_data)

print(user)