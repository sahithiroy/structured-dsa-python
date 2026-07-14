'''
Docstring for python-core-day2.encapsulation
Encapsulation is a fundamental concept in object-oriented programming (OOP) that involves bundling data and methods that operate on that data within a single unit, typically a class.
Encapsulation helps to hide the internal details of an object and only expose the necessary information to the outside world, which can improve security and reduce the risk of errors.
In Python, we can achieve encapsulation by using access modifiers to control the visibility of class attributes and methods. The three main access modifiers in Python are:
1. Public: Attributes and methods that are accessible from anywhere in the program. They are defined without any leading underscores (e.g., attr1, method1).
2. Protected: Attributes and methods that are intended to be accessed only within the class and its subclasses. They are defined with a single leading underscore (e.g., _attr2, _method2).
3. Private: Attributes and methods that are intended to be accessed only within the class itself. They are defined with a double leading underscore (e.g., __attr3, __method3).
By using these access modifiers, we can control the visibility of our class attributes and methods, which can help to prevent unintended access and modification of the internal state of our objects, thus promoting better encapsulation and data integrity in our programs.  
In Python, we can also use property decorators to create getter and setter methods for class attributes, which allows us to control access to the attributes while still providing a way to read and modify their values. 
This is another way to achieve encapsulation in Python.   

'''
# Example of encapsulation in Python
class EncapsulatedClass:    
    def __init__(self, value):
        self.__private_attr = value  # This is a private attribute

    def get_private_attr(self):
        return self.__private_attr  # Getter method to access the private attribute

    def set_private_attr(self, value):
        self.__private_attr = value  # Setter method to modify the private attribute
# Creating an object of the EncapsulatedClass
encapsulated_object = EncapsulatedClass(10) 
# Accessing the private attribute using the getter method
print(encapsulated_object.get_private_attr())  # Output: 10 
# Modifying the private attribute using the setter method
encapsulated_object.set_private_attr(20)
# Accessing the modified private attribute using the getter method
print(encapsulated_object.get_private_attr())  # Output: 20
# Attempting to access the private attribute directly (this will not work)
# print(encapsulated_object.__private_attr)  # This will raise an AttributeError because the private attribute cannot be accessed directly from outside the class.  
'''In this example, we defined a class called EncapsulatedClass with a private attribute __private_attr and two methods, get_private_attr and set_private_attr, which are used to access and modify the private attribute, respectively.
   We created an object of the EncapsulatedClass and used the getter and setter methods to access and modify the private attribute, demonstrating encapsulation in action. 
   We also attempted to access the private attribute directly, which resulted in an AttributeError, showing that the private attribute is not accessible from outside the class.'''

# Example Protected attribute in Python
class ProtectedClass:   
    def __init__(self, value):
        self._protected_attr = value  # This is a protected attribute

    def get_protected_attr(self):
        return self._protected_attr  # Getter method to access the protected attribute
    def set_protected_attr(self, value):
        self._protected_attr = value  # Setter method to modify the protected attribute
# Creating an object of the ProtectedClass
protected_object = ProtectedClass(30)
# Accessing the protected attribute using the getter method
print(protected_object.get_protected_attr())  # Output: 30
# Modifying the protected attribute using the setter method
protected_object.set_protected_attr(40)
# Accessing the modified protected attribute using the getter method

print(protected_object.get_protected_attr())  # Output: 40
# Accessing the protected attribute directly (this is possible but not recommended)

print(protected_object._protected_attr)  # Output: 40 (although it is possible to access the protected attribute directly, it is not recommended as it goes against the principle of encapsulation and can lead to unintended consequences if the attribute is modified directly from outside the class.)

# Example of public attribute in Python
class PublicClass:
    def __init__(self, value):
        self.public_attr = value  # This is a public attribute  \
# Creating an object of the PublicClass
public_object = PublicClass(50) 
# Accessing the public attribute directly
print(public_object.public_attr)  # Output: 50


#Example
class Sahithi:
    def __init__(self,name:str,age :int,salary:float):
        self.name=name
        self._age=age
        self.__salary=salary
    def getDetails(self)->list:
        print(self.name)
        print(self._age)
        
        return [self.name,self._age,self.__salary]
    def modifySalary(self,value):
        self.__salary=value
        return self.__salary
obj1=Sahithi("Sahithi",23,123456)
print(obj1.name)
print(obj1._age)
print(obj1.getDetails())
print(obj1.modifySalary(34566))