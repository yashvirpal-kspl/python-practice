menu=[
    "Masala Chai",
    "Iced lemon Tea",
    "Green Tea",
    "Iced Peach Tea",
    "Ginger Tea"
]

#iced_tea=[tea for tea in menu if "Iced" in tea]
#iced_tea=[my_tea for my_tea in menu if "Iced" in my_tea] #same as loop variable 
#iced_tea=[my_tea for my_tea in menu if len(my_tea)>10]  
iced_tea=[my_tea for my_tea in menu if len(my_tea)<10]  
print(iced_tea)