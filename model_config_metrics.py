import math

filename = "data/GCodeT.txt"

# Count the number of lines in the text file
with open(filename, "r") as file:
    num_lines = sum(1 for line in file)

# Determine an appropriate batch size
# Adjust the batch_size variable based on your resources and preferences
batch_size = 60 # The batch size that you used to trin you model - in the TrainingArguments() (per_device_eval_batch_size=60,)

num_training_steps = math.ceil(num_lines / batch_size)

# Print the calculated values
print("Number of training samples:", num_lines)
print("Batch size:", batch_size)
print(f"Number of training steps: {num_training_steps}")