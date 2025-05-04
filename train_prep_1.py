#%%
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def fizzbuzz_twist():
    for i in range(1, 101):
        if is_prime(i):
            print("Prime", end=" ")
        elif i % 15 == 0:
            print("FizzBuzz", end=" ")
        elif i % 3 == 0:
            print("Fizz", end=" ")
        elif i % 5 == 0:
            print("Buzz", end=" ")
        else:
            print(i, end=" ")

fizzbuzz_twist()

#%%
def is_palindrome(s):
    s = ''.join(filter(str.isalnum, s)).lower()  # Remove spaces and non-alphanumeric characters
    return s == s[::-1]

print(is_palindrome("A man a plan a canal Panama"))  # True


#%%
s = '123456789'

print(s[-1])
# %%
def reverse_string(s):
    reversed_s = ""
    for char in s:
        reversed_s = char + reversed_s
    return reversed_s

print(reverse_string("hello"))  # "olleh"



# %%
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(20)
# %%
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

#%%
#Find Largest and Second Largest


def find_two_largest(numbers):
    largest, second_largest = float('-inf'), float('-inf')
    for num in numbers:
        if num > largest:
            second_largest, largest = largest, num
        elif num > second_largest:
            second_largest = num
    return largest, second_largest

print(find_two_largest([5, 2, 9, 1, 7]))  # (9, 7)

#%%
def sum_of_digits(n):
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

print(sum_of_digits(9876))  # 3

#%%
def count_vowels_consonants(s):
    vowels = "aeiou"
    s = s.lower()
    vowel_count = sum(1 for char in s if char in vowels)
    consonant_count = sum(1 for char in s if char.isalpha() and char not in vowels)
    return vowel_count, consonant_count

print(count_vowels_consonants("Hello World!"))  # (3, 7)



#%%

def multiplication_table():
    for i in range(1, 11):
        for j in range(1, 11):
            print(f"{i * j:3}", end=" ")
        print()

multiplication_table()


# %%
def find_duplicates(lst):
    seen, duplicates = set(), set()
    for num in lst:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    return list(duplicates)

print(find_duplicates([1, 2, 3, 1, 4, 2]))  # [1, 2]



#%%
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

print([num for num in range(1, 51) if is_prime(num)])  # Prime numbers from 1 to 50


#%% 
def find_missing(nums):
    full_set = set(range(1, 101))
    return sorted(full_set - set(nums))

print(find_missing([1, 2, 4, 5, 100]))  # [3, 6, 7, ..., 99]

# %%
def print_pattern():
    for i in range(1, 6):
        print("".join(str(x) for x in range(1, i + 1)))

print_pattern()

# %%
def are_anagrams(s1, s2):
    return sorted(s1.replace(" ", "").lower()) == sorted(s2.replace(" ", "").lower())

print(are_anagrams("listen", "silent"))  # True

# %%
def word_frequencies(s):
    words = s.split()
    frequencies = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies

print(word_frequencies("hello world hello"))  # {'hello': 2, 'world': 1}


# %%
def remove_duplicates(lst):
    return list(dict.fromkeys(lst))

print(remove_duplicates([1, 2, 2, 3, 4, 4]))  # [1, 2, 3, 4]


# %%
def longest_word(sentence):
    words = sentence.split()
    return max(words, key=len)

print(longest_word("The quick brown fox jumps over the lazy dog"))  # "jumps"

# %%
def common_elements(lst1, lst2):
    return list(set(lst1) & set(lst2))

print(common_elements([1, 2, 3], [2, 3, 4]))  # [2, 3]



# %%
def sum_of_multiples(limit):
    return sum(num for num in range(limit) if num % 3 == 0 or num % 5 == 0)

print(sum_of_multiples(1000))  # 233168


#%%
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

print(transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
