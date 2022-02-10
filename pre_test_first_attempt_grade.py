import os
import dill
import pandas as pd

from scripts import pre_test_first_attempt_grade
from util import QUIZ_SCORE_JSON_PATH, CACHE_FOLDER, mkdir_if_not_exists

if __name__ == '__main__':
    GRADE_BOOK_PATH = os.path.join('data', 'processed', 'grade_book.csv')
    grade_book = pd.read_csv(GRADE_BOOK_PATH)
    data448ids = grade_book['ID'].astype('int64')

    pre_test_grade_dict = pre_test_first_attempt_grade(QUIZ_SCORE_JSON_PATH, data448ids)

    mkdir_if_not_exists(CACHE_FOLDER)

    with open(os.path.join(CACHE_FOLDER, 'pre_test_first_attempt_grade_dict.pkl'), 'wb') as f:
        dill.dump(pre_test_grade_dict, f)
