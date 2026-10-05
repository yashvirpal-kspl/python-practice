from enum import Enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field



#OrderStatus (Enum) -> preparing,picked_up,in_transit,delivered
class OrderStatus(str,Enum):
    PREPARING = "preparing"
    PICKED_UP = "piked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

# Database Table for orders
# id(primary key)
# customer_name(str)
# delivery_status(str)
# item (str)
# status (OrderStatus)
# created_At    
# updated_at

class Order(SQLModel,table=True):  
  id: Optional[int] = Field(default=None,primary_key=True)
    customer_name: str = Field(max_length=100)
    delivery_status: str = Field(max_length=100)
    items: str = Field(max_length=100)
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    
#Schema for creating an order
class OrderCreate(SQLModel):
    customer_name: str = Field(max_length=100)
    delivery_status: str = Field(max_length=100)
    items: str = Field(max_length=100)

# Schema for updating an order
class OrderUpdate(SQLModel):
    status: Optional[OrderStatus] = Field(default=None)
    deliver_address: Optional[str] = Field(default=None,max_length=100)
    
# Statuslog schema
class StatusLog(SQLModel):
    order_id: int 
    old_status:str
    new_status:str
    changed_at: datetime = Field(default=datetime.now())
    