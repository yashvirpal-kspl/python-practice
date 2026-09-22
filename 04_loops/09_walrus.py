# value=13
# remainder=value%5

# if remainder:
#     print(f"Not divisble, ramainder is {remainder}")

value=15
if (remainder := value %5):
    print(f"Not divisble, ramainder is {remainder}")
    
# availble_size=["small","medium","large"]
# if(requested_size :=input("Enter your chi cup size: ")) in availble_size:
#     print(f"Serving {requested_size} chai")
# else:
#     print(f"Size is unavailble - {requested_size}")        



flavours=["masala","ginger","lemon","mint"]
print("Availble flavours: ",flavours)

while(flavour :=input("Choose your flavour: ")) not in flavours:
    print(f"Sorry {flavour} is not availble")
    
print(f"You choose {flavour} chai")    