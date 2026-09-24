def encrypt(message,key):
    result=""
    for char in message:
        if char.isalpha():
            base=ord('A') if char.isupper() else ord('a')
            shifted=(ord(char) - base+key) % 26 + base
            result +=chr(shifted)
        else:
            result +=char
    return result     

def decrypt(message,key):
    return encrypt(message,-key)   



print("Secret message program")
choice=input("Do you want to E or D: ").strip().lower()

if choice=='e':
    text=input("Enter your message: \n")
    try:
        key=int(input("Enter a number between 1 and 25: "))
        encrypted=encrypt(text,key)
        print("Encrypted message:")
        print(encrypted)
    except ValueError:
        print("Invalid key")
elif choice == 'd':
    text=input("Enter your message: \n")
    try:
        key=int(input("Enter a number between 1 and 25: "))
        derypted=decrypt(text,key)
        print("Decrypted message:")
        print(derypted)
    except ValueError:
        print("Invalid key")     
else:
    print("Invalid Choice")               