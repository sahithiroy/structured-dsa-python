'''
decorators.py
Decorators are a powerful and elegant way to modify the behavior of functions or classes without changing their source code. They allow you to wrap another function in order to extend its behavior, which can be useful for logging, access control, memoization, and more. 
In python are powerful tools taht allow you to modify the behaviour of functions or classes without changinng the hearts
of the function
Decorators are functions that take another function as an argument and return a new function that can add some kind of functionality to
the orginal function.They are of the form @decorator above the function defination.
Example:
def decorator(func):
    def wrapper(*args,**kwargs):
        print("Before the function call")
        return func(*args,**kwargs)
    return wrapper
'''