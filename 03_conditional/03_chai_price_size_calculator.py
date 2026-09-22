cup_sizes =input("Enter your cup size: ").lower() #BuGer for like this typed

print(f"User Said: {cup_sizes}")

if cup_sizes == 'small':
    print(f"Price is 10 rupees")
elif cup_sizes == 'medium':
    print(f"Price is 15 rupees")
elif cup_sizes == 'large':
    print(f"Price is 20 rupees")        
else:
    print(f"Unknown Cup size")      

      