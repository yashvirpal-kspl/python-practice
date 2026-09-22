# chai ="Ginger Chai"
# def prepare_chai(order):
#     print("Preparing",order)

# prepare_chai(chai)    
# print(chai)    

chai =[1,2,3]

def edit_chai(cup):
    cup[1]=60
edit_chai(chai)  
print(chai)  


def make_chai(tea,milk,sugar):
    print(tea,milk,sugar)
    
make_chai("Darjeeling","Yes","Low")    #positional
make_chai(tea="Green",sugar="Medium",milk="No")    #key words

def special_chai(*ingrediants,**extras):
    print("Ingrediants", ingrediants)
    print("Extras", extras)
    
    
special_chai("cinnamon","cardmom",sweetener="Honey",foam="yes")    
special_chai("cinnamon",type="cardmom",sweetener="Honey",foam="yes")    

# def chai_order(order=[]):
#     order.append("masala")
#     print(order)
def chai_order(order=None):
    if order is None:
        order=[]
    #order.append("masala")
    print(order)
chai_order()    
#chai_order()    