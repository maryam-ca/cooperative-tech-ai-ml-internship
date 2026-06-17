"""
Dataset Profile Analyzer
"""

class DatasetProfile:

    def __init__(
        self,
        file_name,
        source,
        rows,
        columns,
        description
    ):
        self.file_name = file_name
        self.source = source
        self.rows = rows
        self.columns = columns
        self.description = description

    def load_info(self):
        print("\n===== DATASET INFO =====")
        print("File Name:", self.file_name)
        print("Source:", self.source)
        print("Rows:", self.rows)
        print("Columns:", self.columns)

    def display_summary(self):
        print("\nDataset Summary")
        print(self.description)


class CSVDataset(DatasetProfile):

    def get_column_count(self):
        return self.columns


dataset = CSVDataset(
    "students.csv",
    "Kaggle",
    1000,
    15,
    "Student performance analysis dataset."
)

dataset.load_info()
dataset.display_summary()

print(
    "\nTotal Columns:",
    dataset.get_column_count()
)