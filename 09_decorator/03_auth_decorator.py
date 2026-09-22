from functools import wraps

def require_admin(func):
    @wraps(func)
    def wrapper(user_role):
        if user_role != "admin":
            print("Access denied: Admin only")
            return None
        else:
            return func(user_role)    
    return wrapper


@require_admin
def access_tea_inventory(role):
    print(f"Access granted to tea inventory")

access_tea_inventory("admin")
access_tea_inventory("user")