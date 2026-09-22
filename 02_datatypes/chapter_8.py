ingredients=["water","milk","tea"]
ingredients.append("sugar")   #will add in last 
print(f"Ingrediants : {ingredients}")
ingredients.remove("water")
print(f"Ingrediants : {ingredients}")
print(f"#################")
spice_option=["ginger","cardamom"]
chai_ingrdients=["water","milk"]

chai_ingrdients.extend(spice_option)
print(f"chai : {chai_ingrdients}")
chai_ingrdients.insert(2,"black tea") #Will insert in perticular position
print(f"chai : {chai_ingrdients}")
last_added=chai_ingrdients.pop()
print(f"{last_added}")
print(f"chai : {chai_ingrdients}")
chai_ingrdients.reverse()
print(f"chai : {chai_ingrdients}")
chai_ingrdients.sort()
print(f"chai : {chai_ingrdients}")
print("###################")
sugar_levels=[1,2,3,4,5]
print(f"Maximum sugar level : {max(sugar_levels)}")
sugar_levels=[1,32,3,4,5]
print(f"Maximum sugar level : {max(sugar_levels)}")
sugar_levels=[1,32,3,4,5]
print(f"Minimum sugar level : {min(sugar_levels)}")
print("###################")
base_liquid=["water","milk"]
extra_flavor=["ginger"]
full_liquid_mix=base_liquid+extra_flavor
print(f"Liquid Mix: {full_liquid_mix}")

strong_brew=["black tea"] * 3
print(f"Strong Brew: {strong_brew}")
strong_brew=["black tea","water"] * 5
print(f"Strong Brew: {strong_brew}")

raw_spice_data=bytearray(b"Cinnamon")
print(f"Bytes : {raw_spice_data}")
raw_spice_data=raw_spice_data.replace(b"Cinna",b"Card") # it's retrun type 
print(f"Bytes : {raw_spice_data}")