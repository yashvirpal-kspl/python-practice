# Integer
Sugar=10
Milk=15
Total=Sugar+Milk
print(f"Total gram base tea is: {Total}\n")
Total2=Milk-Sugar
print(f"Total Ramian base tea is: {Total2}\n")

milk_in_ltr=7
serve_men=4
milk_per_serving=milk_in_ltr/serve_men
print(f"Milk per serving is {milk_per_serving}\n")

ttl_tea_bags=7
pots=4
bags_per_pot=ttl_tea_bags // pots     ######## 
print(f"While tea bags per pot : {bags_per_pot}\n")

total_cadmom_pods=10
pods_per_cup=3
leftover_pods=total_cadmom_pods % pods_per_cup
print(f"Leftover cadmom pods: {leftover_pods}\n") 

base_flaver_strength=2
scale_factor=3
powerful_flaver=base_flaver_strength ** scale_factor
print(f"Scale Flavour Strength: {powerful_flaver}\n") 

total_tea_leaves_harvested=1_000_000_1000 # we can write it up like for readabilty still count like number
print(f"For Readbality purpose we can write like this : {total_tea_leaves_harvested}")
