order_amount =int(input("Enter the order amount: "))

print(f"Order Amount: {order_amount}")

# Turnary Oprator 
delivery_fee=0 if order_amount >300 else 30

print(f"Delivery fee is : {delivery_fee}")

      