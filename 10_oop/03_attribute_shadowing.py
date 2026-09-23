class Chai:
    tempreture="hot"
    strength="Strong"
 
cutting =Chai()
print(cutting.tempreture)    

cutting.tempreture="mild"
cutting.cup="small"
print("After Changing",cutting.tempreture)
print("Cup SIze is",cutting.cup)
print("Direct look into the class",Chai.tempreture)


del cutting.tempreture
del cutting.cup
print("After Delete from object",cutting.tempreture)
print("After Delete from object",cutting.cup)  # this will not fallback to shadow means in class thats wy it give error
print("Direct look into the class",Chai.tempreture)