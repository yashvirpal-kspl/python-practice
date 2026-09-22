essential_spice={"cardamom","ginger", "cinnamon"}
optional_spice={"clove","ginger", "black paper"}

all_spice= essential_spice | optional_spice
print(f"All Spices : {all_spice}")

common_spice= essential_spice & optional_spice
print(f"Common Spices : {common_spice}")

only_essential_spice= essential_spice - optional_spice
print(f"Essential Spices : {only_essential_spice}")


print(f"Is 'clove' in essential spices ? {'clove' in essential_spice}")
print(f"Is 'clove' in optional spices ? {'clove' in optional_spice}")