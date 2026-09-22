#Boolean
is_boiling=True
stir_count=5
total_action=stir_count+is_boiling    #upcasting
print(f"Total Actions: {total_action}\n")


milk_present= -12 # no milk 
print(f"Is there milk? {bool(milk_present)}\n")
# 0 and None will return false if change it to number or string it will return true even to - value as well

## Logical Opration
hot_water=True
tea_added=False
can_serve=hot_water and tea_added
print(f"Can serve tea? {can_serve}\n")