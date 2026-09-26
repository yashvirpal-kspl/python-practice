import base64
import os

VAULT_FILE = "vault.txt"

def encode(text):
    return base64.b16encode(text.encode()).decode()   #decode is usin for  remove b' from encode () ,Means converting in regular string 


def decode(text):
    return base64.b16decode(text.encode()).decode()  
    
 
def password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)    
    has_lower = any(c.islower() for c in password)    
    has_digit = any(c.isdigit() for c in password) 
    has_special_char = any(c in "!@#$%^&*()_+<>?.," for c in password) 
    
    score = sum([length >= 8, has_upper,has_digit,has_special_char])
    
    return ["Weak","Medium","Strong","Very Strong"][min(score,3)]

def add_credential():
    website = input("Website: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    strength = password_strength(password)
    
    line = f"{website}||{username}||{password}"
    
    encodeed_line = encode(line)
    
    with open(VAULT_FILE,"a",encoding="utf-8" ) as f:
        f.write(encodeed_line + "\n")
    
    print("Credential saved ✅ ")   
    
    
def view_credentials():
    if not os.path.exists(VAULT_FILE):
        print("Vault file not found")
        return
    
    with open(VAULT_FILE,"r",encoding="utf-8") as f:
        for line in f:
            decoded = decode(line.strip())
            website,username,password=decoded.split("||") 
            
            hidden_password = "*" * len(password)
            print(f"{website}|{username}|{password}")     
            
def update_credential():
    
    search_username = input("Search user name: ").strip()
    found = False
    updated_lines = []
    
    with open(VAULT_FILE,"r",encoding="utf-8") as f:
        for line in f:
            decoded = decode(line.strip())
            website,username,password=decoded.split("||") 
            
            if search_username==username:
                website = input("Website: ").strip()
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                
                strength = password_strength(password)
                
                line = f"{website}||{username}||{password}"
                
                encodeed_line = encode(line)
                updated_lines.append(encodeed_line)
                found = True 
            else:
                updated_lines.append(line.strip())    
        if found:        
                
            with open(VAULT_FILE,"w",encoding="utf-8" ) as f:
                for line in updated_lines:
                    f.write(line + "\n")
            print("Credential updated ✅ ")  
        else:
            print("Username does not matched")  
    
       
               
            
def main():
    while True:
        print("\n🔒 Credential Manager\n")
        print("1. Add Credential")
        print("2. View Credentials")
        print("3. Update Credentials")
        print("4. Exit")
        
        choice = input("Choose an option: ").strip()
        
        match choice:
            case "1": add_credential()
            case "2": view_credentials()
            case "3": update_credential()
            case "4": break
            case _: print("Invalid Choice")
                    
if __name__ == "__main__":
    main()                     