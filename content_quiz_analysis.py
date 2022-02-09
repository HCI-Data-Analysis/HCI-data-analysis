from util import ReadingLogsData, pre_test_get_first_attempt_grade, pre_test_first_attempt_grade_average
from scripts import *
import os
import pandas as pd


if __name__ == '__main__':
    QUIZSCOREJSON_PATH = 'data/anonymized/quizzes'
    GRADE_BOOK_PATH = os.path.join('data', 'processed', 'grade_book.csv')
    grade_book = pd.read_csv(GRADE_BOOK_PATH)
    data448ids = grade_book['ID'].astype('int64')
    reading_logs_data = ReadingLogsData()

    # reading_dict, quiz_dict = reading_logs_data.get_parsed_reading_log_data()
    # content_quiz_attempts_analysis()
    content_quiz_grade_analysis(data448ids)
    pre_test_first_attempt_grade_average(QUIZSCOREJSON_PATH, data448ids)