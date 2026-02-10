'''
Docstring for python-core-day2.
managerRequirements:

Extra attribute: bonus

Override get_annual_salary() to include bonus

Reuse parent logic (don’t copy-paste)

👉 Be ready to explain:

super()

Why inheritance is appropriate here
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
class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus
    def get_annual_salary(self):
        base_salary = super().get_annual_salary()  # Reuse parent logic to get base annual salary
        return base_salary + self.bonus  # Add bonus to the base salary to get total annual salary
# Example usage
manager = Manager('Alice', 8000, 5000)