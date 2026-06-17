"""
Dataset Analysis Tool
Handles multiple exceptions.
"""

dataset = {
    "students": 500,
    "teachers": 30
}

try:

    file_name = input("Enter dataset name: ")

    if file_name == "":
        raise ValueError("Dataset name cannot be empty.")

    print(dataset[file_name])

except KeyError:
    print("ERROR: Dataset key not found.")

except ValueError as error:
    print("ERROR:", error)

except TypeError:
    print("ERROR: Invalid data type.")

finally:
    print("Analysis Completed.")