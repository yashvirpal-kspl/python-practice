names=["Yash","Prince","John","Mike" ]
bills=[40,60,10,100]

for name,amount in zip(names,bills): # zip  combine two list same iteraion 
    print(f"{name} : {amount} ruppees")