"""
Machine Learning Accuracy Calculator
Handles division by zero.
"""

def calculate_accuracy(correct_predictions, total_predictions):
    """
    Calculate model accuracy.
    """

    try:
        accuracy = (correct_predictions / total_predictions) * 100
        print(f"Accuracy: {accuracy:.2f}%")

    except ZeroDivisionError:
        print("ERROR: Total predictions cannot be zero.")

    finally:
        print("Calculation Finished.")


calculate_accuracy(90, 100)
calculate_accuracy(50, 0)