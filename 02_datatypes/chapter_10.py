chai_order=dict(type="Masal Chai",size="Large",sugar=2)
print(f"Chai Order : {chai_order}")

chai_recipe={}
chai_recipe['base']="Black Tea"
chai_recipe['liquid']="Milk"

print(f"Recipe Base : {chai_recipe['base']}")
print(f"Recipe : {chai_recipe}")
del chai_recipe['liquid']
print(f"Recipe : {chai_recipe}")


print(f"Is sugar in chai order : {'sugar' in chai_order}")


print("#######################")
chai_order=dict(type="Ginger Chai",size="Large",sugar=2)
print(f"Chai Order : {chai_order}")
print(f"order detail (keys) : {chai_order.keys()}")
print(f"order detail (values) : {chai_order.values()}")
print(f"order detail (items) : {chai_order.items()}")
print("#######################")
last_item=chai_order.popitem()
#last_item=chai_order.pop('sugar')
print(f"Remove last item : {last_item}")
print(f"Remaining Chain Order : {chai_order}")

extra_spices={"cardamom":"crushed","ginger":"sliced"}
chai_recipe.update(extra_spices)
print(f"Chai Recipe updated is : {chai_recipe}")
print("#######################")
chai_size=chai_order["size"] #if exist key
print(f"Chai size is : {chai_size}") 
customer_note=chai_order.get("customer_note","No Note") #if might not exist key set 2nd value
print(f"Customer note is : {customer_note}")