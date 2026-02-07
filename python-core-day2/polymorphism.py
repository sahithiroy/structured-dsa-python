'''
Docstring for python-core-day2.polymorphism
Polymorphism is a fundamental concept in object-oriented programming (OOP) that allows objects of different classes to be treated as if they were of the same class.
This is achieved through method overriding, where a subclass provides a specific implementation of a method that is
already defined in its superclass.
Polymorphism allows for flexibility and extensibility in code, as it enables us to write code that can work with objects of different types without needing to know their specific class.
In Python, polymorphism can be achieved through duck typing, which means that the type of an object is determined by its behavior rather than its class.
This allows us to write code that can work with any object that implements the required methods, regardless
'''
# Example of polymorphism in Python
class Animal:
    def speak(self):
        pass    
class Dog(Animal):
    def speak(self):
        return "Woof!"
class Cat(Animal):
    def speak(self):
        return "Meow!"
# Creating objects of the Dog and Cat classes
dog = Dog()
cat = Cat()
# Using polymorphism to call the speak method on both objects   
print(dog.speak())  # Output: Woof!
print(cat.speak())  # Output: Meow!
# In this example, we have a superclass called Animal with a method called speak that is defined but not implemented.
# We then have two subclasses, Dog and Cat, that inherit from the Animal class and provide their own implementation of the speak method.
# We create objects of both the Dog and Cat classes and call the speak method on each object.
# Because of polymorphism, we can call the speak method on both objects without needing to know their specific class, and the correct implementation of the method will be executed based on the type of the object.



'''   Runtime polymorphism vs compile-time polymorphism
Runtime polymorphism, also known as dynamic polymorphism, occurs when the method to be executed is determined at runtime based on the type of the object.
Compile-time polymorphism, also known as static polymorphism, occurs when the method to be executed is determined at compile time based on the type of the reference variable.
In Python, we primarily use runtime polymorphism through method overriding, as Python is a dynamically typed language. 
However, we can also achieve compile-time polymorphism through method overloading, 
which is not natively supported in Python but can be implemented using default arguments or variable-length arguments.'''


#method overriding in inheritance
'''Method overriding is a feature in object-oriented programming (OOP) that allows a child class to provide a specific implementation of a method that is already defined in its parent class.
When a method in a child class has the same name and signature as a method in its parent class, the child class's method will override the parent class's method.
This allows the child class to provide a different behavior for the method while still maintaining the same interface.
Method overriding is commonly used to customize or extend the functionality of inherited methods in a child class.

Rules for method overriding:
1. The method in the child class must have the same name as the method in the parent class.
2. The method in the child class must have the same number and type of parameters as the method in the parent class.
3. The method in the child class can have a different implementation than the method in the parent class, but it must maintain the same interface (i.e., the same method signature).
4. The method in the child class can call the method in the parent class using the super() function if it needs to access the parent class's implementation of the method.
Method overriding is a powerful feature that allows for polymorphism and dynamic method dispatch in OOP, enabling objects of different classes to be treated as instances of the same class while still providing specific behavior based on their actual class type.
In Python, we can override a method in a child class by simply defining a method with the same name as the method in the parent class. When we call the method on an object of the child class, the child class's implementation will be executed instead of the parent class's implementation.'''
#Example of method overriding in Python


class Parent:
    def display(self):
        print("This is the display method in the Parent class.")
class Child(Parent):
    def display(self):
        print("This is the display method in the Child class.")
# Creating an object of the Child class
child_object = Child()
child_object.display()  # Output: This is the display method in the Child class.

'''In this example, we have a Parent class with a display method and a Child class that inherits from the Parent class and overrides the display method.
When we create an object of the Child class and call the display method, the implementation in the Child class is executed, demonstrating method overriding.
Method overriding allows us to provide specific behavior in the child class while still maintaining the same method signature as the parent class, enabling polymorphism and dynamic method dispatch in our code.   
'''
#method overriding with super() function
class Parent:
    def display(self):
        print("This is the display method in the Parent class.")    
class Child(Parent):
    def display(self):
        super().display()  # Call the display method of the Parent class
        print("This is the display method in the Child class.")
# Creating an object of the Child class
child_object = Child()
child_object.display()
#output:
# This is the display method in the Parent class.   
# This is the display method in the Child class.










#method overloading in inheritance
'''Method overloading is a feature in object-oriented programming (OOP) that allows a class to have multiple methods with the same name but different parameters. 
When a method is called, the appropriate method is selected based on the number and types of arguments passed to it. This allows for more flexible and intuitive code, as the same method name can be used to perform different operations based on the context.    
In Python, method overloading is not natively supported as it is in some other programming languages. However, we can achieve similar functionality using default parameters, *args, and **kwargs to allow for a variable number of arguments.'''
class A:
    def add(self, x, y):
        return x + y
    def add(self, x, y, z):
        return x + y + z
obj1 = A()
print(obj1.add(2, 3))      # This will raise a TypeError because the method with two parameters has been overridden by the method with three parameters.
print(obj1.add(2, 3, 4))   # Output: 9

# To avoid this issue, we can use default parameters in the method definition to allow for both cases using multipledispatch.
from multipledispatch import dispatch
class A:
    @dispatch(int, int)
    def add(self, x, y):
        return x + y
    @dispatch(int, int, int)
    def add(self, x, y, z):
        return x + y + z
obj1 = A()
print(obj1.add(2, 3))      # Output: 5  
print(obj1.add(2, 3, 4))   # Output: 9

#using args and kwargs to handle method overriding
class A:
    def add(self, *args):
        if len(args) == 2:
            return args[0] + args[1]
        elif len(args) == 3:
            return args[0] + args[1] + args[2]
obj1 = A()
print(obj1.add(2, 3))      # Output: 5  
print(obj1.add(2, 3, 4))   # Output: 9







#Give an scenario it is better to use inheritance in programming?
'''
Scenario: A company has a software system that manages different types of employees,
 such as full-time employees, part-time employees, and contractors.
 Each type of employee has common properties like name, ID, and department, 
 as well as specific behaviors related to their employment type (e.g., calculating salary, tracking hours worked, etc.).'''

# In this scenario, we can use inheritance to create a base class called Employee that contains the common properties and behaviors shared by all types of employees.
# Then, we can create child classes for each specific type of employee (FullTimeEmployee, PartTimeEmployee, Contractor) that inherit from the Employee class and implement their own specific behaviors.
class Employee:
    def __init__(self, name, employee_id, department):
        self.name = name
        self.employee_id = employee_id
        self.department = department

    def calculate_salary(self):
        pass  # This method will be overridden in the child classes
class FullTimeEmployee(Employee):
    def calculate_salary(self):
        return 5000  # Example fixed salary for full-time employees
class PartTimeEmployee(Employee):
    def calculate_salary(self):
        return 20 * 40  # Example hourly wage for part-time employees (20 per hour, 40 hours per week)
class Contractor(Employee):
    def calculate_salary(self):
        return 1000  # Example fixed payment for contractors
# Creating objects of each employee type
full_time_employee = FullTimeEmployee("Alice", "FT123", "Engineering")
part_time_employee = PartTimeEmployee("Bob", "PT456", "Marketing")
contractor = Contractor("Charlie", "CT789", "Design")
# Accessing properties and calculating salary for each employee
print(full_time_employee.name)  # Output: Alice
print(full_time_employee.calculate_salary())  # Output: 5000    
print(part_time_employee.name)  # Output: Bob
print(part_time_employee.calculate_salary())  # Output: 800

print(contractor.name)  # Output: Charlie
print(contractor.calculate_salary())  # Output: 1000
'''In this example, we have a base class Employee that contains common properties and a method calculate_salary that is meant to be overridden by the child classes.
   The FullTimeEmployee, PartTimeEmployee, and Contractor classes inherit from the Employee class and provide their own implementations of the calculate_salary method based on their specific employment type.
   This use of inheritance allows us to avoid code duplication and maintain a clear and organized structure for our employee management system. 
   It also makes it easier to add new types of employees in the future by simply creating new child classes that inherit from the Employee class. 
'''