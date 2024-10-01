# Python Object-Oriented Programming Example

# Class representing a Family Member
class Fam:
    def __init__(self, name, surname, age):
        """
        Initializes a family member with a name, surname, and age.
        It also generates an email for the member.

        Parameters:
        name (str): First name of the family member
        surname (str): Last name of the family member
        age (int): Age of the family member
        """
        self.name = name
        self.surname = surname
        self.age = age
        self.mail = name + '.' + surname + str(age) + '@mail.ru'  # Generate email dynamically

# Creating a family member
mem_1 = Fam("Daler", "Khamidov", 23)

# Printing the generated email for the family member
print(mem_1.mail)

#%% Employee Class with Class Variables

class Employee:
    """
    A class to represent an employee in an organization.
    """
    raise_amount = 1.04  # Default raise amount
    num_of_emp = 0  # Class variable to track the number of employees

    def __init__(self, first, last, pay):
        """
        Initialize the employee with their first name, last name, and salary.

        Parameters:
        first (str): First name of the employee
        last (str): Last name of the employee
        pay (float): Salary of the employee
        """
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'  # Employee email
        Employee.num_of_emp += 1  # Increment employee count

    def fullname(self):
        """
        Returns the full name of the employee.
        """
        return f'{self.first} {self.last}'

    def apply_raise(self):
        """
        Apply a salary raise based on the class's raise_amount.
        """
        self.pay = int(self.pay * self.raise_amount)

# Example usage of the Employee class
emp_1 = Employee("Daler", "Khamidov", 500)
emp_2 = Employee("Tima", "Ataj", 600)

print(emp_1.pay)  # Output the pay of employee 1

#%% Class Methods and Alternative Constructors

class Employee:
    raise_amount = 1.04
    num_of_emp = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'
        Employee.num_of_emp += 1

    def fullname(self):
        return f'{self.first} {self.last}'

    def apply_raise(self):
        self.pay = int(self.pay * Employee.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        """
        Class method to set the raise amount for all employees.
        """
        cls.raise_amount = amount

    @classmethod
    def from_string(cls, emp_str):
        """
        Alternative constructor that creates an Employee object from a string.

        Parameters:
        emp_str (str): Employee data in the format 'First-Last-Pay'
        """
        first, last, pay = emp_str.split('-')
        return cls(first, last, int(pay))

# Example of creating an employee from a string
emp_str_1 = 'Daler1-Khamidov-4500'
new_emp_1 = Employee.from_string(emp_str_1)

# Set new raise amount for all employees
Employee.set_raise_amt(1.1)

print(new_emp_1.pay)  # Output the salary of the new employee

#%% Static Methods

class Employee:
    num_of_emp = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'
        Employee.num_of_emp += 1

    def fullname(self):
        return f'{self.first} {self.last}'

    def apply_raise(self):
        self.pay = int(self.pay * Employee.raise_amount)

    @staticmethod
    def is_workday(day):
        """
        Static method to check if a given date is a workday.
        """
        return day.weekday() not in (5, 6)  # Returns False if it's Saturday(5) or Sunday(6)

# Example of using the static method
import datetime
my_date = datetime.date(2020, 12, 3)
print(Employee.is_workday(my_date))

#%% Inheritance Example (Developer and Manager Classes)

class Developer(Employee):
    def __init__(self, first, last, pay, prog_lang):
        """
        Inherit properties from Employee and add a programming language.
        """
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang

class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        """
        Inherit from Employee and manage a list of employees.
        """
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        """
        Add an employee to the manager's team.
        """
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        """
        Remove an employee from the manager's team.
        """
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emp(self):
        """
        Print all the employees managed by the manager.
        """
        for emp in self.employees:
            print('-->', emp.fullname())

# Example usage of Developer and Manager classes
dev_1 = Developer("Daler", "Khamidov", 500, 'Python')
emp_2 = Employee('Tima', "Ataj", 600)
mng_1 = Manager('Xasan', 'Ishankulov', 32000, [dev_1])
mng_1.add_emp(emp_2)

print(dev_1.prog_lang)  # Output the programming language
mng_1.print_emp()  # Print the employees managed by the manager

#%% Special Methods (Dunder Methods)

class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    def __repr__(self):
        return f"Employee('{self.first}', '{self.last}', {self.pay})"

    def __str__(self):
        return f'{self.fullname()} - {self.email}'

    def __add__(self, other):
        """
        Allows adding the pay of two employees using + operator.
        """
        return self.pay + other.pay

    def __len__(self):
        """
        Returns the length of the employee's full name.
        """
        return len(self.fullname())

# Special methods in action
emp_1 = Employee("Daler", "Khamidov", 500)
emp_2 = Employee("Tima", "Ataj", 600)

print(emp_1 + emp_2)  # Output the sum of the pays
print(repr(emp_1))  # Output the formal string representation
print(str(emp_1))  # Output the informal string representation
print(len(emp_1))  # Output the length of the full name

#%% Property Decorators - Getters, Setters, and Deleters

class Employee:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def email(self):
        """
        Generates an email based on the first and last name.
        """
        return f'{self.first}.{self.last}@mail.ru'

    @property
    def fullname(self):
        """
        Returns the full name.
        """
        return f'{self.first} {self.last}'

    @fullname.setter
    def fullname(self, name):
        """
        Set the first and last name using a single string.
        """
        first, last = name.split(' ')
        self.first = first
        self.last = last

    @fullname.deleter
    def fullname(self):
        """
        Delete the first and last name.
        """
        print('Delete Name!')
        self.first = None
        self.last = None

# Example of using property methods
emp_1 = Employee("Daler", "Khamidov")
emp_1.fullname = 'Zafar Zugurov'  # Use the setter to update name
del emp_1.fullname  # Use the deleter to clear the name

print(emp_1.first)
print(emp_1.email)
print(emp_1.fullname)
