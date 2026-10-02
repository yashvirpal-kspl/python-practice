from pydantic import BaseModel


class User(BaseModel):  #
    id:int
    name:str
    is_active:bool
    
input_data ={"id":101,"name":"Yash","is_active":23}    

user =User(**input_data)  ## this is updacked dicktionory

print(f"{user}")