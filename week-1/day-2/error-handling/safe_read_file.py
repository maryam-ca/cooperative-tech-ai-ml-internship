"""
Advanced File Reader
Provides file statistics.
"""

def safe_read_file(file_path):

    try:

        with open(file_path, "r") as file:

            content = file.read()

            if not content.strip():
                print("WARNING: File is empty.")
                return

            lines = content.splitlines()
            words = content.split()

            print("\n===== FILE REPORT =====")
            print("File Name:", file_path)
            print("Total Lines:", len(lines))
            print("Total Words:", len(words))
            print("Total Characters:", len(content))

    except FileNotFoundError:
        print("ERROR: File not found.")

    finally:
        print("Reading Process Completed.")


safe_read_file("sample.txt")