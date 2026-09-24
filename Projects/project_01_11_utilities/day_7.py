import os

TASK_FILE="tasks.txt"

def load_tasks():
    tasks=[]
    if(os.path.exists(TASK_FILE)):
        with open(TASK_FILE,'r',encoding="utf-8") as f:
            for line in f:
                text,status=line.strip().rsplit("||",1)
                tasks.append({"text":text,"done":status=="done"})
    return tasks

def save_tasks(tasks):
    with open(TASK_FILE , "w", encoding="utf-8") as f:
        for task in tasks:
            status= "done" if task["done"] else "not done"   
            f.write(f"{task['text']} || {status}\n") 
            
def display_tasks(tasks):
    if not tasks:
        print(f"No task found")
    else:
        for i,task in enumerate(tasks,1):
            checkbox="✅ " if task["done"] else ""
            print(f"{i}. [{checkbox}] {task['text']}")     
    print("*"*20)
    
def task_manager():
    tasks=load_tasks()
    
    while True:
        print("\n--------Task List Manager-----------")  
        print("1. Add task")                       
        print("2. View tasks")                       
        print("3. Mark task as complete")                       
        print("4. Delete task")                       
        print("5. Exit task")                       
        
        choice=input("Choos an option (1-5)").strip()       
        
        match choice:
            case "1":
                text=input("Enter your task").strip()
                if text:
                    tasks.append({"text":text,"done":False})
                    save_tasks(tasks)
                else:
                    print("Task can not be empty")            
            
            case "2":
                display_tasks(tasks)
            case "3":
                display_tasks(tasks)
                try:
                    num=int(input("Enter task number")) 
                    if 1<=num <=len(tasks):
                        tasks[num-1]["done"]=True       
                        save_tasks(tasks)
                        print("task mark as done")
                    else:
                        print("Invalid Task number")
                except ValueError:
                    print("Please enter a number")
            case "4":
                display_tasks(tasks)
                try:
                    num=int(input("Enter task number to delete")) 
                    if 1<=num <=len(tasks):
                        removed=tasks.pop(num-1)     
                        save_tasks(tasks)
                        print(f"task removed {removed} and there text is {removed['text']}")
                    else:
                        print("Invalid Task number")
                except ValueError:
                    print("Please enter a number")     
            case "5":
                print("Exiting task manager")
                break
            case _:
                print("Please choose valid task")
                
                
task_manager()                
                            