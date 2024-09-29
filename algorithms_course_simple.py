# The following code snippets demonstrate various programming constructs in Python,
# including loops, conditionals, random number generation, sorting algorithms, and recursion.

# Printing numbers in a grid pattern.
# For n in range (7):
#    for m in range(4):
#        print(n,end=" ")
#    print()
#
# for n in range(4):
#     for m in range(10):
#         print(m+1, end=" ")
#     print()

# Print the number 5, n times, where n is the current value of n.
# for n in range(6):
#     for m in range(n):
#         print(5, end=" ")
#     print()

# Print 0, n times, where n is decreasing from 5 to 2.
# for n in range(5,1,-1):
#     for m in range(n):
#         print(0, end=" ")
#     print()

# Print the multiplication table from 0 to 9.
# for n in range(10):
#     for m in range(10):
#         a= n*m
#         print(n,"*",m,"=",a,"    ", end=" ")
#     print()

#%%

from random import random, randint
import time

# Ask for the number of rounds N.
N = int(input("N="))
igrok_1 = input("Your name:")
igrok_2 = input("Your name")
mat1 = 0
mat2 = 0

# Play N rounds of a dice game between two players.
for k in range(N):
    k = k + 1
    print("%s Round" % k)
    input("Go 1 player")
    time.sleep(1)
    a = randint(1, 6)
    b = randint(1, 6)
    rez1 = a + b
    print("1GAMER score: (%s,%s)" % (a, b))
    
    input("Go 2 player")
    time.sleep(1)
    c = randint(1, 6)
    d = randint(1, 6)
    rez2 = c + d
    print("2GAMER score: (%s:%s)" % (c, d))
    
    # Determine the winner based on scores.
    if rez1 > rez2:
        print("First player won with score: %s:%s" % (rez1, rez2))
        mat1 += 1
    elif rez1 == rez2:
        print("Drawing")
    else:
        mat2 += 1
        print("Second player won with score: %s:%s" % (rez1, rez2))

time.sleep(1)
print("Match result %s:%s / Winner: Diyor" % (mat1, mat2))

#%%

from random import random, randint

# The computer selects a number between 0 and 100.
x = randint(0, 100)
print("The computer has selected a number from 0 to 100. What number?")
n = 0

# Continue until the user guesses the number.
while True:
    n = n + 1
    y = int(input("Enter a number from 0 to 100. X = "))

    if y > x:
        print("Incorrect. The number is less than %s. Try another number:" % (y))
    elif y < x:
        print("Incorrect. The number is greater than %s. Try another number:" % (y))
    else:
        print("Correct! Congratulations!")
        break

print("You guessed the number in %s attempts. The number was %s." % (n, x))

#%%

from random import random, randint

# Function for playing a simple guessing game.
def parti():
    N = int(input("N="))
    d = 0  # Wins for the player
    e = 0  # Wins for the computer

    for n in range(N):
        n = int(input("n="))
        b = 0  # Player wins
        c = 0  # Computer wins

        for k in range(n):
            while True:
                rez = int(input('k='))
                if rez != 1 and rez != 2:
                    print("Please enter a valid number.")
                else:
                    break
            
            a = randint(1, 2)
            print(a)

            # Determine if the player won this round.
            if rez == a:
                b = b + 1
                print("You won this round.")
            else:
                c = c + 1
                print("Unlucky.")

        print("Player:Computer %s:%s " % (b, c))
        if b > c:
            d = d + 1
            print("You won this game.")
        else:
            print("The computer won this game.")
            e = e + 1

    # Final result of the match.
    if d > e:
        print("You won the match with a score of %s:%s" % (d, e))
    else:
        print("You lost the match with a score of %s:%s" % (d, e))

parti()

#%%

# Input size of array N.
N = int(input())
A = [0] * N  # Initialize list A of size N.
B = [0] * N  # Initialize list B of size N.

# Fill array A with user input.
for k in range(N):
    A[k] = int(input())

# Element-wise copying from A to B.
for k in range(N):
    B[k] = A[k]

# Copying arrays
# C = A  # This creates a reference, not a copy.
# Creating a new list C.
C = list(A)

A[2] = 100  # Modify A to demonstrate that C and B are unaffected.
print(A, B)
print(C)

#%%

# Function to invert an array.
def invert_array(A: list, N: int):
    for k in range(N // 2):
        A[k], A[N - 1 - k] = A[N - 1 - k], A[k]

# Testing the invert_array function.
def test_invert_array():
    A1 = [0, 1, 2, 3, 4, 5]
    print(A1)
    invert_array(A1, 6)
    print(A1)
    if A1 == [5, 4, 3, 2, 1, 0]:
        print('test=ok')
    else:
        print('test-fail')

    A2 = [0, 0, 0, 0, 0, 0, 0, 10]
    print(A2)
    invert_array(A2, 8)
    print(A2)
    if A2 == [10, 0, 0, 0, 0, 0, 0, 0]:
        print('test - ok')
    else:
        print('test- fail')

test_invert_array()

#%%

# Function to shift elements of an array to the right.
def fg(A: list, N: int):
    tmp = A[N - 1]  # Store the last element.
    for k in range(N - 2, -1, -1):
        A[k + 1] = A[k]  # Shift elements to the right.
    A[0] = tmp  # Place the last element at the beginning.
    print(A)

fg([1, 2, 3], 3)

#%%
# Insertion sort algorithm.
def insert_sort(A):
    N = len(A)
    for top in range(1, N):
        k = top
        while k > 0 and A[k - 1] > A[k]:
            A[k], A[k - 1] = A[k - 1], A[k]  # Swap elements.
            k -= 1

# Selection sort algorithm.
def choice_sort(A):
    N = len(A)
    for pos in range(0, N - 1):
        for k in range(pos + 1, N):
            if A[k] < A[pos]:
                A[k], A[pos] = A[pos], A[k]  # Swap elements.

# Bubble sort algorithm.
def buble_sort(A):
    N = len(A)
    for bypass in range(1, N):
        for k in range(0, N - bypass):
            if A[k] > A[k + 1]:
                A[k], A[k + 1] = A[k + 1], A[k]  # Swap elements.

# Test sorting algorithms.
def test_sort(sort_algorithm):
    print("Test #1 ", end="")
    A = [4, 3, 5, 2, 1]
    A_sorted = [1, 2, 3, 4, 5]
    sort_algorithm(A)  # Apply sorting algorithm.
    print("OK" if A_sorted == A else "FAIL")
    print(A_sorted, ":", A)

test_sort(insert_sort)
test_sort(choice_sort)
test_sort(buble_sort)

#%%

import unittest
from arithmetic_arranger import arithmetic_arranger

# The test case for arithmetic_arranger function.
class UnitTests(unittest.TestCase):
    def test_arrangement(self):
        actual = arithmetic_arranger(["3 + 855", "3801 - 2", "45 + 43", "123 + 49"])
        expected = "  3      3801      45      123\n" \
                    "+ 855   -    2   + 43   + 49\n" \
                    "-----    ------    -----    -----\n" \
                    " 858      3799      88      172"
        self.assertEqual(actual, expected)

# More test cases can be added as needed.
