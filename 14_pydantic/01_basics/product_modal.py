from pydantic import BaseModel


class Product(BaseModel):  #
    id:int
    name:str
    price:float
    in_stock:bool =True  #if pass then then passed value else this take this default value
    
# product_one ={"id":1,"name":"Laptop","price":999.99,"in_stock":True}    
# product_two ={"id":2,"name":"Mobile","price":93.90,"in_stock":True} 
product_one =Product(id=1,name="Laptop",price=999.99,in_stock=True)   
product_two =Product(id=1,name="Mobile",price=25.67)     
#product_three =Product(name="Mobile")  #Give Error     


