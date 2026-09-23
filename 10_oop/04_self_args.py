class Chaicup:
    size=10 #ml
    
    def describe(self):
        return f"A {self.size}ml chai cup"        
 
cup =Chaicup()
print(cup.describe())    
print(Chaicup.describe(cup))    
#print(Chaicup.describe())    # will give error because Self keyword in class only work for object created 


cup_two=Chaicup()
cup_two.size=100
print(Chaicup.describe(cup_two)) 