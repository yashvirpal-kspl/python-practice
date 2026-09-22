staff=[("Yash",30),("Zigane",17),("Ray",40)]
for name,age in staff:
    if age >= 18:
        print(f"{name} eligible to manage staff")
        break   #if not use break keyword else will run always
else:  # this only run if loop does not use break 
    print("No one is able to manage staff")        