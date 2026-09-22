menu=[
    "Masala Chai",
    "Iced lemon Tea",
    "Green Tea",
    "Iced Peach Tea",
    "Ginger Tea",
    "Green Tea",
]
#unique_chai={chai for chai in menu }
unique_chai={chai for chai in menu if len(chai) > 8}
unique_chai={chai for chai in menu if len(chai) < 8}
print(unique_chai)

recipes={
    "Masala Chai":["Ginger","cardamom","clove"],
    "Elaichi Chai":["milk","cardamom"],
    "Spicy Chai":["Ginger","black paper","clove"],
}

unique_recipes={spice for ingrediants in recipes.values() for spice in ingrediants}  # both loop will go expression 
print(unique_recipes)