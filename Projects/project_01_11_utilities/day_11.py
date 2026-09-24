def friendship_score(name1,name2):
    name1,name2=name1.lower(),name2.lower()
    score = 0
    shared_letters = set(name1) & set(name2)
    vowels = set('aeiou')
    
    score += len(shared_letters) * 5
    score = len(vowels & shared_letters) * 10
    
    return min(score,100)

def run_frienship_calculator():
    print("♥️ Friendship Compatibilty calculator ♥️")
    name1 = input("Enter First Name: ")
    name2 = input("Enter Second Name: ")
    
    score = friendship_score(name1,name2)
    print(f"\n{score}")
    
    
run_frienship_calculator()    