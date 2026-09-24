def calculate_minutes(age_years):
    DAYS_IN_YEARS=365.25
    HOURS_IN_DAY=24
    MINUTES_IN_HOUR=60
    
    total_days=age_years * DAYS_IN_YEARS
    total_hours=total_days * HOURS_IN_DAY
    total_minuts= total_hours * MINUTES_IN_HOUR
    
    return round(total_days), round(total_hours), round(total_minuts)

while True:
    try:
        age=float(input("Enter Your age in years: "))
        days,hours,minuts=calculate_minutes(age)
        
        print("\nYour are approx:")
        print(f" - {days} days old")
        print(f" - {hours} hours old")
        print(f" - {minuts} minuts old")
        
        
        again=input("would you like to try again? (y/n)").strip().lower()
        if again != 'y':
            print("Good Bye!")
            break
        
    except ValueError:
        print("Please provide age in number")    