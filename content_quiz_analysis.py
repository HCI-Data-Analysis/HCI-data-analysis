from util import ReadingLogsData
from scripts import content_quiz_grade_analysis, content_quiz_attempts_analysis
import os
import pandas as pd


if __name__ == '__main__':

    GRADE_BOOK_PATH = os.path.join('data', 'processed', 'grade_book.csv')
    grade_book = pd.read_csv(GRADE_BOOK_PATH)
    data448ids = grade_book['ID'].astype('int64')

    reading_logs_data = ReadingLogsData()

    reading_dict, quiz_dict = reading_logs_data.get_parsed_reading_log_data()
    # content_quiz_attempts_analysis()
    content_quiz_grade_analysis(data448ids)
