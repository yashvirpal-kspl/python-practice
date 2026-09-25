def collect_student_data():
    students={}
    
    while True:
        name = input("Enter the student name or done to exit: ").strip()
        if name.lower() == 'done':
            break
        if name in students:
            print("Student already exist")
            continue
        try:
            marks = float(input(f"Enter marks for {name}: "))
            students[name] = marks
        except ValueError:
            print("Please enter a valid number for marks")    
    
    return students     
def display_report(students):
    if not students:
        print("no student data found")
        return
    
    marks= list(students.values())
    max_score = max(marks)
    min_score = min(marks)
    average = sum(marks) / len(marks)
    
    topper_scorer = [name for name,score in students.items() if score == max_score]
    bottom_scorer = [name for name,score in students.items() if score == min_score]
    average_scorer = [name for name,score in students.items() if score == average]
    
    print("\n Students mark report")
    
    print("-" * 20)
    
    print(f"Total students: {len(students)}")
    print(f"Average marks for students: {average:.2f}")
    print(f"Highest Score: {max_score} by {(", ".join(topper_scorer))}")
    print(f"Lowest Score: {min_score} by {(", ".join(bottom_scorer))}")
    
    print("-" * 20)
    
    print("Detailed Marks")
    for name,score in students.items():
        print(f" - {name}: {score}")
        
students = collect_student_data()        
display_report(students)
    