tea_price_inr={
    "Masala Chai":40,
    "Elaichi Chai":50,
    "Spicy Chai":300,
}
# Doller convert 
unique_recipes={tea:price/92 for tea,price in tea_price_inr.items()} 
print(unique_recipes)