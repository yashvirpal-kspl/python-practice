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