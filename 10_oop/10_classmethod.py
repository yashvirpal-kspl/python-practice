class ChaiOrder:
    def __init__(self,tea_type,sweetness,size):
        self.tea_type=tea_type
        self.sweetness=sweetness
        self.size=size
    
    @classmethod
    def form_dict(cls,order_data):   #cls s keyword refrence to class with decorator
        return cls(
            order_data["tea_type"],
            order_data["sweetness"],
            order_data["size"],
        )
        
    @classmethod
    def form_string(cls,order_string):   
        tea_type,sweetness,size=order_string.split("-")
        return cls(tea_type,sweetness,size)
    
class ChaiUtils:
    @staticmethod
    def is_valid_size(size):
        return size in ["Small","Medium", "Large"]  
    
print(ChaiUtils.is_valid_size("Mediumq"))      
print(ChaiUtils.is_valid_size("Medium"))      
    
order=ChaiOrder.form_dict({"tea_type":"masala","sweetness":"medium","size":"Large"})
order2=ChaiOrder.form_string("Ginger-Low-Small")    
order3=ChaiOrder("Lemon","High","Medium")    

print(order)
print(order2)

print(order.__dict__)
print(order2.__dict__)
print(order3.__dict__)