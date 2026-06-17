"""
User Input Validation System
Handles invalid numeric input.
"""

def get_age():
    """
    Get age from user safely.
    """

    try:
        age = int(input("Enter your age: "))

        if age < 0:
            raise ValueError("Age cannot be negative.")

        print("Age:", age)

    except ValueError as error:
        print("Invalid Input:", error)

    finally:
        print("Input Process Completed.")


get_age()