"""
Student Dataset Analyzer
"""

import csv


def analyze_students():

    marks = []

    top_student = ""
    highest_marks = 0

    with open("students.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            student_marks = int(row["marks"])

            marks.append(student_marks)

            if student_marks > highest_marks:
                highest_marks = student_marks
                top_student = row["name"]

    average_marks = sum(marks) / len(marks)

    print("\n===== STUDENT ANALYSIS =====")
    print("Total Students:", len(marks))
    print("Average Marks:", round(average_marks, 2))
    print("Top Student:", top_student)
    print("Highest Marks:", highest_marks)


analyze_students()