number_poeple=int(input("How many people ae there in group? "))

names=[]

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌Please enter valid number. ")    

for i in range(number_poeple):
    name=input(f"Enter the name of person #{i+1}: ").strip()
    names.append(name)
    
 
total_bill=get_float("Enter the bill amount in number only: ")

share = round(total_bill/number_poeple)


print("\n" + "*" * 40)
print(f"Total bill: {total_bill}")
print(f"Each person owes: {share}")


for name in names:
    print(f"{name} owes {share} rupees")
    
print("\n" + "*" * 40)    
    