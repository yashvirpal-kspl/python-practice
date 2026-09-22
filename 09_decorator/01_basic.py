from functools import wraps  # For Name Print passing function 
def  my_decorator(func):   # pass wunction as parameter
    @wraps(func)
    def wrappper():
        print("Before function run")
        func()
        print("After function run")
    return  wrappper
@my_decorator
def greet():
    print("hello from decorator use")

greet()    
print(greet.__name__)
    