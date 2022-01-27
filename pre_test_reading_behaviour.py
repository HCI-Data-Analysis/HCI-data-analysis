import pandas as pd

from scripts import pre_test_reading_behaviour_analysis

GRADEBOOK_PATH = 'data/anonymized/grade_book.csv'

if __name__ == '__main__':
    gradebook = pd.read_csv(GRADEBOOK_PATH)
    pre_test_reading_behaviour_analysis(gradebook)
