# def numbers():
#     yield 1
#     # yield 2
#     # yield 3

# for num in numbers():
#     print(num)
#     print("sssssss")
    
# def my_generator():
#     print("First")
#     yield 10

#     print("Second")
#     yield 20

# gen = my_generator()

# print(next(gen))
# print(next(gen))    

#################################
from functools import wraps

def my_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Function started")

        result = func(*args, **kwargs)

        print("Function finished")

        return result

    return wrapper


@my_decorator
def add(a, b):
    return a + b


print(add(10, 20))