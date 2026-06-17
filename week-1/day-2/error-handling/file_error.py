"""
File Error Handling Example
Checks whether dataset file exists.
"""

def load_dataset(file_path):
    """
    Load dataset file safely.
    """

    try:
        with open(file_path, "r") as file:
            print("Dataset Loaded Successfully")
            print(file.read())

    except FileNotFoundError:
        print("ERROR: Dataset file not found.")
        print("Please check file path.")

    finally:
        print("Operation Completed.")


load_dataset("sales_data.csv")