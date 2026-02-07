'''
Docstring for python-core-day2.oopsIntroduction

oops stands for Object Oriented Programming System. 
It is a programming paradigm that uses objects and classes to structure code in a 
way that is more modular, reusable, and easier to maintain.
It also says that it is a programming paradigm that uses objects and classes to structure code in a 
way that is more modular, reusable, and easier to maintain.
class is a blueprint for creating objects. 
It defines the properties and behaviors of the objects that will be created from it.
properties are the attributes or characteristics of an object, 
while behaviors are the actions or methods that an object can perform.
In OOP, we can create multiple objects from a single class, 
and each object can have its own unique properties and behaviors.
why we are using classes and objects in programming?
1. Modularity: Classes allow us to break down complex problems into smaller, more manageable pieces
2. Reusability: Once we have defined a class, we can create multiple objects from it, which can save us time and effort in writing code.
3. Encapsulation: Classes allow us to hide the internal details of an object and only expose the necessary information to the outside world, which can help to improve security and reduce the risk of errors.
4. Inheritance: Classes can be used to create new classes that inherit properties and behaviors from existing classes, which can help to reduce code duplication and improve code organization.
5. Polymorphism: Classes can be designed to allow objects of different types to be treated as if they were of the same type, which can help to improve code flexibility and reduce the need for complex conditional statements. 
'''
# Example of a class and object in Python
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start_engine(self):
        print("The engine is starting...")
# Creating an object of the Car class
my_car = Car("Toyota", "Camry", 2020) 

# Accessing properties of the object
print(my_car.make)  # Output: Toyota    
print(my_car.model) # Output: Camry
print(my_car.year)  # Output: 2020
# Calling a method of the object
my_car.start_engine()  # Output: The engine is starting...  

'''In this example, we defined a class called Car with an __init__ method that initializes the properties of the car
 (make, model, and year) and a method called start_engine that simulates starting the car's engine.
   We then created an object of the Car class called my_car and accessed its properties and called its method.



   what is the __init__ method in Python? why we are using it in classes?

The __init__ method in Python is a special method that is called when an object is created from a class. 
It is used to initialize the properties of the object with the values passed as arguments when the object is created.
The __init__ method is defined within a class and takes at least one parameter, which is usually named self.
The self parameter refers to the instance of the object being created and allows us to access and modify the properties of the object within the method.
We use the __init__ method in classes to ensure that when an object is created, it is initialized with the necessary properties and values.
This helps to ensure that the object is in a valid state and can be used effectively in our program. 
Without the __init__ method, we would have to manually set the properties of the object after it is created, which can lead to errors and inconsistencies in our code.'''

class SampleClass:
    attr1=10
    attr2=20
obj1=SampleClass()
print(obj1.attr1) # Output: 10
print(obj1.attr2) # Output: 20
obj1.attr1=30
print(obj1.attr1) # Output: 30
SampleClass.attr1=40
print(SampleClass.attr1) # Output: 40
print(obj1.attr1) # Output: 30
#why it is not changing the value of attr1 for obj1 when we change it for SampleClass?
# Because obj1 has its own instance attribute attr1 that shadows the class attribute attr1.expalination:
# When we create an object of a class, it can have its own instance attributes that can shadow the class attributes. In this case, obj1 has its own instance attribute attr1 that was set to 30.
# When we change the value of attr1 for the SampleClass, it does not affect the instance attribute attr1 of obj1 because it is a separate attribute that belongs to the object, not the class. 
# Therefore, when we print obj1.attr1, it still shows the value of 30, which is the value of the instance attribute, rather than the value of the class attribute.