from scripts import performance_by_activity_type

FILE_PATH = "data/anonymized/grade_book.csv"

if __name__ == "__main__":
    performance_by_activity_type(FILE_PATH, 2)  # call the method on the gradebook with 2 standard deviations
