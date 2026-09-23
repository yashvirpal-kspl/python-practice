class Chaiorder:
    def __init__(self,type_,size):
        self.type=type_
        self.size=size
    
    def summary(self):
        return f"{self.size}ml of {self.type} chai"        
 
cup =Chaiorder('Masala',200)
print(cup.summary())    


cup2 =Chaiorder('Ginger',250)
print(cup2.summary())   
