#%%

# Example of using lists to store and display student names and grades.
students = []
grades = []

# Collecting student names and grades.
for i in range(3):
    name = input("Enter student name: ")
    grade = int(input("Enter grade for {}: ".format(name)))
    students.append(name)
    grades.append(grade)

# Displaying student names and grades.
print("\nStudent Grades:")
for i in range(len(students)):
    print("{}: {}".format(students[i], grades[i]))

#%%

# Function to check if a number is prime.
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Testing the prime checking function.
for num in range(1, 21):
    if is_prime(num):
        print(f"{num} is a prime number.")

#%%

# Function to generate Fibonacci sequence up to n terms.
def fibonacci(n):
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

# Generate and print the Fibonacci sequence.
n_terms = 10
print(f"Fibonacci sequence with {n_terms} terms: {fibonacci(n_terms)}")

#%%

# Function to reverse a string.
def reverse_string(s):
    return s[::-1]

# Test the reverse_string function.
input_string = input("Enter a string to reverse: ")
print("Reversed string:", reverse_string(input_string))

#%%

# Simple implementation of a countdown timer.
import time

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(i, end=" ", flush=True)
        time.sleep(1)
    print("Time's up!")

# Run a countdown timer for 5 seconds.
countdown_timer(5)

#%%

# Simple implementation of a calculator.
def calculator():
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    else:
        return "Invalid operator!"

# Get result from calculator.
result = calculator()
print("Result:", result)

#%%

# Function to find the maximum number in a list.
def find_maximum(numbers):
    max_number = numbers[0]
    for num in numbers:
        if num > max_number:
            max_number = num
    return max_number

# Test the find_maximum function.
test_numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print("Maximum number in the list:", find_maximum(test_numbers))

#%%

# Function to create a simple histogram from a list of numbers.
def histogram(data):
    for value in data:
        print('*' * value)

# Test the histogram function.
test_data = [1, 3, 5, 2, 4]
print("Histogram:")
histogram(test_data)

#%%

# Function to count vowels in a string.
def count_vowels(s):
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

# Test the count_vowels function.
input_text = input("Enter a sentence: ")
print("Number of vowels:", count_vowels(input_text))

#%%

# Function to create a simple list of squares from 1 to n.
def list_of_squares(n):
    return [i**2 for i in range(1, n + 1)]

# Test the list_of_squares function.
n = 10
print("List of squares from 1 to {}: {}".format(n, list_of_squares(n)))
