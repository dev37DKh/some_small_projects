#%%
import numpy as np

# Create NumPy arrays
a = np.array([1, 2, 3])  # 1D array
b = np.array([[1, 23, 4], [2, 34, 6]])  # 2D array

# Print properties of the arrays
print(b.ndim)  # Number of dimensions of array b
print(a.shape)  # Shape of array a
print(a.dtype)  # Data type of array a
print(a.itemsize)  # Size of each element in bytes

# Get a specific element from a 2D array
print(b[1, 2])  # Access element in the second row and third column of b

# Create arrays filled with zeros
print(np.zeros((3, 2)))  # 3x2 array of zeros

# Create arrays filled with ones
print(np.ones(3))  # 1D array of three ones

# Create an array filled with a specified number
print(np.full((2, 3), 7))  # 2x3 array filled with 7

# Create an array full like another array with a specified value
print(np.full_like(a, 44))  # Array like a, filled with 44

# Create an array of random decimal numbers
print(np.random.rand(4, 2))  # 4x2 array of random numbers in [0, 1)

# Create an array of random integers
print(np.random.randint(2, 4, size=(3, 2)))  # 3x2 array of random integers between 2 and 4

# Create and manipulate a matrix
output = np.ones((5, 5))  # 5x5 array of ones
z = np.zeros((3, 3))  # 3x3 array of zeros
z[1, 1] = 9  # Set the middle element of z to 9
output[1:4, 1:4] = z  # Insert z into a slice of output
print(output)  # Print the modified output

# Create a copy of an array
a = np.array([1, 3, 4])
b = a.copy()  # Create a copy of a
print(b)  # Print the copied array

# Perform mathematical operations with NumPy
g = np.cos(a)  # Take the cosine of elements in a
print(g)  # Print the result of the cosine operation

#%%
# Matrix multiplication example
a = np.ones((2, 3))  # 2x3 array of ones
b = np.full((3, 2), 2)  # 3x2 array filled with 2
c = np.matmul(a, b)  # Matrix multiplication
print(c)  # Print the result of the multiplication

# Find the determinant of a matrix
d = np.identity(3)  # 3x3 identity matrix
print(np.linalg.det(d))  # Print the determinant of d

#%%
# Working with statistics
stats = np.array([1, 2, 3])
print(stats)  # Print the stats array
min_val = np.min(stats)  # Find the minimum value
print(min_val)  # Print the minimum value

# Reorganizing arrays
before = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])  # Original 2D array
print(before.shape)  # Print the shape of before
after = before.reshape((2, 2, 2))  # Reshape to 2x2x2 array
print(after)  # Print the reshaped array

#%%
# Vertical stacking of vectors
v1 = np.array([1, 2, 3, 4])
v2 = np.array([5, 6, 7, 8])
d = np.vstack([v1, v2, v1, v2])  # Stack v1 and v2 vertically
print(d)  # Print the stacked array

# Horizontal stacking (hstack)
# Example:
# h = np.hstack([v1, v2])  # Stack v1 and v2 horizontally
# print(h)  # Print the horizontally stacked array

# Load data from a file (Make sure 'data.txt' exists)
# np.genfromtxt('data.txt', delimiter=',')  # Load data with specified delimiter

# Boolean Masking and Advanced indexing
# Example usage:
# mask = (stats > 1)  # Create a boolean mask
# print(stats[mask])  # Print elements where the mask is True
