daily_sales=[5,10,12,34,50,40,9]


total_cups=(sale for sale in daily_sales if sale >5)
print(total_cups)   # give object of generator

total_cups=sum(sale for sale in daily_sales if sale >5)
print(total_cups)  