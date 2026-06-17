"""
Text File Analyzer
Reads file and generates statistics.
"""

def analyze_file(file_name):

    try:

        with open(file_name, "r") as file:

            content = file.read()

            total_lines = len(content.splitlines())
            total_words = len(content.split())
            total_characters = len(content)

            print("\n===== FILE ANALYSIS REPORT =====")
            print("File Name:", file_name)
            print("Total Lines:", total_lines)
            print("Total Words:", total_words)
            print("Total Characters:", total_characters)

    except FileNotFoundError:
        print("File Not Found")


analyze_file("daily_log.txt")