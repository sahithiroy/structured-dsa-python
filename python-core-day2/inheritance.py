'''
Docstring for python-core-day2.inheritance

Inheritance is a fundamental concept in object-oriented programming (OOP) that allows a new class (called a child or subclass) 
to inherit properties and behaviors from an existing class (called a parent or superclass).
The child class can then add its own properties and behaviors or override the inherited ones to provide specific functionality.
Inheritance promotes code reusability and helps to create a hierarchical relationship between classes, making it easier to organize and manage code in larger applications.
In Python, we can define a child class that inherits from a parent class using the following syntax
'''
# Example of inheritance in Python
class ParentClass:
    def parent_method(self):
        print("This is a method in the parent class.")  
class ChildClass(ParentClass):
    def child_method(self):
        print("This is a method in the child class.")   

# Creating an object of the ChildClass
child_object = ChildClass() 
# Accessing the method from the parent class
child_object.parent_method()  # Output: This is a method in the parent class.   
# Accessing the method from the child class
child_object.child_method()   # Output: This is a method in the child class.
#i'm trying accessing the parent class method using the child class object and it is working fine. 
# but parrent object to access the child method is not working. why?
# Creating an object of the ParentClass
parent_object = ParentClass()   
# Accessing the method from the child class using the parent object (this will not work)
# parent_object.child_method()  # This will raise an AttributeError because the parent class does not have access to the child class's method.

'''In this example, we defined a ParentClass with a method called parent_method. We then defined a ChildClass that inherits from ParentClass and has its own method called child_method.
   We created an object of the ChildClass and were able to access both the parent_method from the ParentClass and the child_method from the ChildClass, demonstrating inheritance in action.''' 

'''
Types of Inheritance in Python
1. Single Inheritance: A child class inherits from a single parent class.   
2. Multiple Inheritance: A child class inherits from multiple parent classes.
3. Multilevel Inheritance: A child class inherits from a parent class, which in turn inherits from another parent class, creating a multi-level hierarchy.
4. Hierarchical Inheritance: Multiple child classes inherit from a single parent class.
5. Hybrid Inheritance: A combination of two or more types of inheritance, such as multiple and multilevel inheritance.
'''

# Example of single inheritance
class Animal:
    def eat(self):
        print("This animal is eating.") 
class Dog(Animal):
    def bark(self):
        print("The dog is barking.")
# Creating an object of the Dog class
dog_object = Dog() 
# Accessing the method from the parent class
dog_object.eat()  # Output: This animal is eating.  
# Accessing the method from the child class
dog_object.bark() # Output: The dog is barking.

# Example of multiple inheritance
class Father:
    def father_method(self):
        print("This is a method in the Father class.")  
class Mother:
    def mother_method(self):
        print("This is a method in the Mother class.")
class Child(Father, Mother):
    def child_method(self):
        print("This is a method in the Child class.")
# Creating an object of the Child class
child_object = Child()  
# Accessing methods from both parent classes
child_object.father_method()  # Output: This is a method in the Father class.   
child_object.mother_method()  # Output: This is a method in the Mother class.
# Accessing the method from the child class
child_object.child_method()   # Output: This is a method in the Child class.
# what hapens if both parent class have same method name and we are calling that method using child class object? 
# which method will be called? 
# how to call the method of specific parent class in that case?
# If both parent classes have the same method name and we call that method using the child class object, Python will follow the method resolution order (MRO) to determine which method to call.
# The MRO is determined by the order in which the parent classes are listed in the child class definition. In this case, the method from the first parent class (Father) will be called.
# To call the method of a specific parent class, we can use the class name to specify which method we want to call. 
# For example, to call the common method from the Father class, we can use Father.common_method(child_object), and to call the common method from the Mother class, we can use Mother.common_method(child_object).

class Father:
    def common_method(self):
        print("This is the common method in the Father class.") 
class Mother:
    def common_method(self):
        print("This is the common method in the Mother class.")
class Child(Father, Mother):
    def child_method(self):
        print("This is a method in the Child class.")
# Creating an object of the Child class
child_object = Child()  
# Accessing the common method (this will call the method from the Father class due to the method resolution order)
child_object.common_method()  # Output: This is the common method in the Father class.

# To call the method of a specific parent class, we can use the class name to specify which method we want to call
# Calling the common method from the Father class   
Father.common_method(child_object)  # Output: This is the common method in the Father class.
# Calling the common method from the Mother class   
Mother.common_method(child_object)  # Output: This is the common method in the Mother class.


'''In this example, we demonstrated single inheritance with the Animal and Dog classes, and multiple inheritance with the Father, Mother, and Child classes.
   We also showed how to handle method name conflicts in multiple inheritance by specifying the parent class when calling the method.
'''

#Example of multilevel inheritance
class Grandparent:
    def grandparent_method(self):
        print("This is a method in the Grandparent class.") 
class Parent(Grandparent):
    def parent_method(self):
        print("This is a method in the Parent class.")
class Child(Parent):
    def child_method(self):
        print("This is a method in the Child class.")
# Creating an object of the Child class
child_object = Child()  
# Accessing methods from all levels of the hierarchy
child_object.grandparent_method()  # Output: This is a method in the Grandparent class.   
child_object.parent_method()        # Output: This is a method in the Parent class. 
child_object.child_method()         # Output: This is a method in the Child class.
'''In this example, we demonstrated multilevel inheritance with the Grandparent, Parent, and Child classes.
   The Child class inherits from the Parent class, which in turn inherits from the Grandparent class.
   We created an object of the Child class and accessed methods from all levels of the hierarchy.
'''

# Example of hierarchical inheritance
class Parent:
    def parent_method(self):
        print("This is a method in the Parent class.")  
class Child1(Parent):
    def child1_method(self):
        print("This is a method in the Child1 class.")
class Child2(Parent):
    def child2_method(self):
        print("This is a method in the Child2 class.")
# Creating objects of the Child1 and Child2 classes
child1_object = Child1()
child2_object = Child2()
# Accessing the method from the parent class using Child1 object
child1_object.parent_method()  # Output: This is a method in the Parent class.
# Accessing the method from the parent class using Child2 object
child2_object.parent_method()  # Output: This is a method in the Parent class.
# Accessing methods from the child classes
child1_object.child1_method()  # Output: This is a method in the Child1 class.
child2_object.child2_method()  # Output: This is a method in the Child2 class.
'''In this example, we demonstrated hierarchical inheritance with the Parent, Child1, and Child2 classes.
   Both Child1 and Child2 inherit from the Parent class.
   We created objects of both child classes and accessed the parent class method as well as their own methods.
'''

# Example of hybrid inheritance
class Base: 
    def base_method(self):
        print("This is a method in the Base class.")    
class Derived1(Base):
    def derived1_method(self):
        print("This is a method in the Derived1 class.")    
class Derived2(Base):
    def derived2_method(self):
        print("This is a method in the Derived2 class.")
class Hybrid(Derived1, Derived2):
    def hybrid_method(self):
        print("This is a method in the Hybrid class.")
# Creating an object of the Hybrid class
hybrid_object = Hybrid()    
# Accessing methods from all parent classes
hybrid_object.base_method()      # Output: This is a method in the Base class.  
hybrid_object.derived1_method()  # Output: This is a method in the Derived1 class.  
hybrid_object.derived2_method()  # Output: This is a method in the Derived2 class.  
# Accessing the method from the Hybrid class    
hybrid_object.hybrid_method()    # Output: This is a method in the Hybrid class.
'''In this example, we demonstrated hybrid inheritance with the Base, Derived1, Derived2, and Hybrid classes.
   The Hybrid class inherits from both Derived1 and Derived2, which in turn inherit from the Base class.
   We created an object of the Hybrid class and accessed methods from all parent classes as well as its own method.
'''

#How to remove the duplicate code in the child class if both parent class have same method name and we are calling that method using child class object?
# We can use the super() function to call the method from the parent class and avoid code duplication in the child class.   

