def process_order(item,quantity):
    try:
        price={"masala":20}[item]
        print(type (price),type(quantity))
        cost=int(price)*int(quantity)
      #  cost=price*quantity
        print(f"Total cost is {cost}")
    except KeyError:
        print(f"Sorry That chai is not on menu") 
    except TypeError:
        print(f"Quantity must be in number")   
    except ValueError:
            print(f"Quantity must be in number")         
        
        
process_order("ginger",2)      # Key Error [item] do not match masala with ginger which ii pass  
process_order("masala",2)   
process_order("masala","two")        