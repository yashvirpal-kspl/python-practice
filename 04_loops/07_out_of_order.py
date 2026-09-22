flavours=["Ginger","Out of Stock","Lemon","Discontinued","Tulsi"]
for flavour in flavours:
    if flavour=="Out of Stock":
        continue
    if flavour =="Discontinued":
        print(f"{flavour} item found")
        break
    
print (f"Out side of loop")    