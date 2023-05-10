import numpy as np

# Create the input array with shape (5, 1, 100)
input_array = np.random.rand(5, 1, 20)

# Convert the array to shape (5, 100)
output_array = np.squeeze(input_array)

# Print the shapes of the input and output arrays
print("Input array shape:", input_array)
print("Output array shape:", output_array)
