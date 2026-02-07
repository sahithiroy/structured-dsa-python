'''
Docstring for python-core-day2.dataHiding
Data hiding is a fundamental concept in object-oriented programming (OOP) that involves restricting access to certain data or attributes of an object to prevent unauthorized access and modification.
Data hiding helps to protect the internal state of an object and ensures that it can only be accessed through well-defined interfaces (methods).    
In Python, we can achieve data hiding by using access modifiers to control the visibility of class attributes. ]
Private attributes are defined with a double leading underscore (e.g., __private_attr) and are intended to be accessed only within the class itself.
'''
# Example of data hiding in Python
class DataHidingClass:
    def __init__(self, value):
        self.__hidden_data = value  # This is a private attribute that is hidden from outside the class

    def get_hidden_data(self):
        return self.__hidden_data  # Getter method to access the hidden data

    def set_hidden_data(self, value):
        self.__hidden_data = value  # Setter method to modify the hidden data   
# Creating an object of the DataHidingClass
data_hiding_object = DataHidingClass(50)
# Accessing the hidden data using the getter method
print(data_hiding_object.get_hidden_data())  # Output: 50
# Modifying the hidden data using the setter method
data_hiding_object.set_hidden_data(100) 
# Accessing the modified hidden data using the getter method
print(data_hiding_object.get_hidden_data())  # Output: 100
# Attempting to access the hidden data directly (this will not work)
# print(data_hiding_object.__hidden_data)  # This will raise an AttributeError because the hidden data cannot be accessed directly from outside the class.  
'''In this example, we defined a class called DataHidingClass with a private attribute __hidden_data and two methods, get_hidden_data and set_hidden_data, which are used to access and modify the hidden data, respectively.
   We created an object of the DataHidingClass and used the getter and setter methods to access and modify the hidden data, demonstrating data hiding in action. 
   We also attempted to access the hidden data directly, which resulted in an AttributeError, showing that the hidden data is not accessible from outside the class.'''
