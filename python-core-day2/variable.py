'''
Docstring for python-core-day2.variable
Instance variable vs static variable
Instance variables are variables that are defined within a class and are unique to each instance of the class. They are typically initialized in the __init__ method of the class and can be accessed and modified using the self keyword. Each instance of the class will have its own copy of the instance variable, allowing for different values to be stored for each object.
Static variables, on the other hand, are variables that are shared among all instances of a class
How to access a static variable in Python?
In Python, you can access a static variable (also known as a class variable) using the class name or through an instance of the class. 
Here are two ways to access a static variable:
1. Using the class name:
   You can access a static variable directly through the class name without creating an instance of the class. For example:
   ```python
   class MyClass:
       static_variable = "This is a static variable"

   # Accessing the static variable using the class name
   print(MyClass.static_variable)  # Output: This is a static variable
   ```
2. Using an instance of the class:
you can also access a static variable through an instance of the class. 
However, it is important to note that when you access a static variable through an instance, it will still refer to the same static variable shared by all instances of the class. 
For example:
```python
class MyClass:  
    static_variable = "This is a static variable"   
# Creating an instance of the class
my_instance = MyClass()
# Accessing the static variable through an instance
print(my_instance.static_variable)  # Output: This is a static variable
'''

#static variable example
class MyClass:  
    static_variable = "This is a static variable"
# Accessing the static variable using the class name
print(MyClass.static_variable)  # Output: This is a static variable
# Creating an instance of the class
my_instance = MyClass()

# Accessing the static variable through an instance
print(my_instance.static_variable)  # Output: This is a static variable 


#instance variable example
class MyClass:  
    def __init__(self, value):
        self.instance_variable = value  # This is an instance variable      
# Creating two instances of the class with different values for the instance variable
instance1 = MyClass("This is instance 1")
instance2 = MyClass("This is instance 2")
# Accessing the instance variable for each instance
print(instance1.instance_variable)  # Output: This is instance 1
print(instance2.instance_variable)  # Output: This is instance 2


'''StaticMethod vs InstanceMethod
Static methods are methods that belong to a class rather than an instance of the class.
They are defined using the @staticmethod decorator and do not have access to the instance (self) or class (cls) variables. 
Static methods are typically used for utility functions that do not require access to instance or class data.
Instance methods, on the other hand, are methods that belong to an instance of a class and have access to the instance (self) variables. 
They are defined without any decorators and can modify the state of the instance. Instance methods are typically used for operations that require access to instance data or behavior.
In summary, static methods are associated with the class and do not have access to instance data, while instance methods are associated with an instance and have access to instance data. '''

#give an example of static method and instance method in python
class MyClass:
    class_variable = "This is a class variable"

    @staticmethod
    def static_method():
        return "This is a static method"

    def instance_method(self):
        return f"This is an instance method and the class variable is: {self.class_variable}"
# Accessing the static method using the class name
print(MyClass.static_method())  # Output: This is a static method   
# Creating an instance of the class
my_instance = MyClass() 
# Accessing the instance method through the instance
print(my_instance.instance_method())  # Output: This is an instance method and the class variable is: This is a class variable


#when we use static method and when we use instance method in python?
# We use static methods when we want to define a method that does not require access to instance data or behavior. 
# Static methods are typically used for utility functions that perform a specific task and do not depend on the state of the instance. 
# For example, a static method could be used to perform a calculation or to format a string.
# We use instance methods when we want to define a method that requires access to instance data or behavior.
# Instance methods are typically used for operations that modify the state of the instance or that depend on the state of the instance.
#  For example, an instance method could be used to update the attributes of an object or to perform an action that is specific to that instance.  