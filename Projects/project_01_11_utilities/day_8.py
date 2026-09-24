import string
import random
import getpass

def check_password_strength(password):
    issues=[]
    if len(password)<8:
        issues.append("To short (minimum 8 characters)")
    if not any(c.islower() for c in password):
        issues.append("Missing lower case letter")
    if not any(c.isupper() for c in password):
        issues.append("Missing uppar case letter")   
    if not any(c.isdigit() for c in password):
        issues.append("Missing a digit")
    if not any(c in string.punctuation for c in password):
        issues.append("Missing a special character")
    return issues        
            
            
def generate_strong_pasword(length=12):
    chars=string.ascii_letters+string.digits+string.punctuation
    
    return "".join(random.choice(chars) for _ in range(length)) 


password=getpass.getpass("Enter a password: ")   
issues=check_password_strength(password)                             
            
if not issues:
    print("Strong Password! you are good to go") 
else:
    print("You got week password")
    for issue in issues:
        print(f" - {issue}") 
        
suggeston=generate_strong_pasword()       
print("\nSuggesting you a strong password")         
print(suggeston) 


###################### 
import string
print(string.ascii_letters)     
print(string.ascii_lowercase)     
print(string.ascii_uppercase)    
print(string.digits)    
print(string.capwords(s="gggggggggggg ttttttt hhhhhhh"))    
print(string.hexdigits)    
print(string.octdigits)    
print(string.punctuation)    
print(string.printable)    