'''
Docstring for python-core-day2.abstraction
Abstraction is a fundamental concept in object-oriented programming (OOP) that involves hiding the complex implementation details of an object and exposing only the necessary features and functionalities to the user.
Abstraction allows us to focus on what an object does rather than how it does it, which can help to simplify our code and make it easier to use and maintain.
In Python, we can achieve abstraction by using abstract classes and interfaces. An abstract class is a class that cannot be instantiated and is meant to be subclassed by other classes.
It can contain abstract methods, which are methods that are declared but not implemented in the abstract class. 
Subclasses of the abstract class must provide an implementation for the abstract methods.
An interface is a collection of abstract methods that define a contract for what a class can do, without specifying how it does it.
 A class that implements an interface must provide an implementation for all the methods defined in the interface.
By using abstraction, we can create more flexible and modular code that can be easily extended and modified without affecting the overall structure of our program. It also helps to improve code readability and maintainability by hiding unnecessary details and providing a clear and concise interface for users to interact with our objects.
'''
# Example of abstraction in Python using abstract classes
from abc import ABC, abstractmethod 
class AbstractClass(ABC):
    @abstractmethod
    def abstract_method(self):
        pass  # This is an abstract method that must be implemented by subclasses   
class ConcreteClass(AbstractClass):
    def abstract_method(self):
        print("This is the implementation of the abstract method in the ConcreteClass.")                                
# Creating an object of the ConcreteClass
concrete_object = ConcreteClass()
# Calling the abstract method, which is implemented in the ConcreteClass
concrete_object.abstract_method()  # Output: This is the implementation of the abstract method in the ConcreteClass.
'''In this example, we defined an abstract class called AbstractClass with an abstract method called abstract_method. We then defined a ConcreteClass that inherits from AbstractClass and provides an implementation for the abstract method.
   We created an object of the ConcreteClass and called the abstract method, which is implemented in the ConcreteClass, demonstrating abstraction in action. 
   The user of the ConcreteClass does not need to know how the abstract method is implemented; they only need to know that it can be called and will provide the expected functionality.'''

''''
Encapsulation vs abstraction vs datahiding vs messageParsing
Encapsulation:wrapping of data and methods is called encapsulation.
Abstraction: hiding the implementation details and showing only functionality to the user is called abstraction.
Data hiding: hiding the data members of a class is called data hiding.
message parsing: it is a process of converting a message from one format to another format. 
It is used in communication between different systems or applications to ensure that 
the data being exchanged is in a format that can be understood by both parties. 
Message parsing can involve various techniques such as tokenization, syntax analysis, and semantic analysis to extract meaningful information 
from the message and convert it into a usable format for further processing.'''