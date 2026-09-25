import csv
import os

FILENAME="contacts.csv"
if not os.path.exists(FILENAME):
    with open(FILENAME,"w",newline="" ,encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name","Phone","Email"])
        
def add_contact():
    name = input("Name: ").strip()        
    phone = input("Phone: ").strip()        
    email = input("Email: ").strip()        
    
    #Check for duplicate
    with open(FILENAME,"r", newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Name"].lower() == name.lower():
                print("Contact name alread exist")
                return
    
    with open(FILENAME,"a", newline="",encoding="utf-8") as f:
        writer=csv.writer(f)
        writer.writerow([name,phone,email])
        print("Contact Added with: ",name,email,phone)  
           
        
        
def view_contacts():
    with open(FILENAME,"r" ,  newline="", encoding="utf-8") as f:
        reader = csv.reader(f)         
        rows = list(reader)
        # print(rows)
        # return
        if len(rows) < 2:
            print("\n No Contact found \n")
            return
        print("\n Your Contacts: \n")
        for row in rows[1:]:  # Skip First row header
            print(f"{row[0]} | {row[1]} | {row[2]}") 
        print()     
            
            
def search_contact():
    term = input("Enter the name to search: ").strip().lower()
    found = False
    
    with open(FILENAME,"r" , newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if term in row["Name"].lower():
                print(f"{row["Name"]} - {row["Phone"]} - {row["Email"]}")            
                found =True
    if not found:
        print("No matching contact found")           

def update_contact():
    term = input("Enter the name to update: ").strip().lower()
    found=False
    with open(FILENAME,"r" , newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
       
    for row in rows:
        if term in row["Name"].lower():
            print(f"\n[MATCH FOUND] Updating: {row['Name']}")
            name = input("Name: ").strip()        
            phone = input("Phone: ").strip()        
            email = input("Email: ").strip()
            row["Name"] = name
            row["Phone"] = phone
            row["Email"] = email  
            found=True   
               
    if found:
        with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print("\nFile updated successfully!")
    else:
        print("\nNo matching contact found.")


def remove_contact():
    term = input("Enter the name to remove: ").strip().lower()
    found=False
    with open(FILENAME,"r" , newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    new_rows = []   
    for row in rows:
        if term in row["Name"].lower():
            print(f"\n[MATCH FOUND] Removing: {row['Name']}")
            found=True 
            continue  
        new_rows.append(row)
               
    if found:
        with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)
        print("\contact remove successfully!")
    else:
        print("\nNo matching contact found.")
        
def main():
    while True:
        print("\n Contact Book \n")
        print("1. Add Contact")        
        print("2. View all Contacts")        
        print("3. Search Contact")        
        print("4. Update Contact")        
        print("5. Remove Contact")        
        print("6. Exit")
        
        choice = input("Choose option (1-6): ").strip()
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice =="3":
            search_contact()
        elif choice =="4":
            update_contact()
        elif choice =="5":
            remove_contact()                
        elif choice == "6":
            print("Thank for choosing our software")
            break                   
        else:
            print("Invalid Choice number")
            
if __name__ == "__main__":
    main()            