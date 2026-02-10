'''
Docstring for python-core-day2.Employee
Requirements:

Attributes:

name (string)

salary (positive number)

Methods:

get_annual_salary()

apply_raise(percent)

Rules:

Salary cannot be negative

Raise percent must be > 0

Handle invalid input gracefully
'''

class Employee:
    def __init__(self, name, salary):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")

        if not isinstance(salary, (int, float)) or salary <= 0:
            raise ValueError("Salary must be a positive number")

        self.name = name
        self.salary = salary

    def get_annual_salary(self):
        return self.salary * 12

    def apply_raise(self, percent):
        if percent <= 0:
            raise ValueError("Raise percent must be greater than 0")

        self.salary += self.salary * (percent / 100)
        return self.salary
obj1=Employee('sahithi',10000)
print(obj1.get_annual_salary())
print(obj1.apply_raise(10))