import datetime
name=input("What is your name: ").strip()
age=input("How old are you: ").strip()
city=input("Whic city do you live in: ").strip()
proffesion=input("What is your profession: ").strip()
hobby=input("What is your favourite hobby: ").strip()


intro_message=(
    f"Hello! my name is {name}, I'm {age} years old and live in {city}"
    f"I work as a {proffesion} and I absolutely enjoy {hobby} in my free time" 
    f"Nice to meet you!\n"
)


current_date=datetime.date.today().isoformat()
intro_message += f"\nLogged on: {current_date}"


border="*"*80
final_output =f"{border}\n{intro_message}\n{border}"

print(final_output)