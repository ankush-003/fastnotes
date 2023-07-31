def my_Decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper
def say_hi():
    print("Hi!")
say_hi = my_Decorator(say_hi)
say_hi()

# Decorator syntax
@my_Decorator
def say_hi2():
    print("Hi! using decorator syntax")

say_hi2()