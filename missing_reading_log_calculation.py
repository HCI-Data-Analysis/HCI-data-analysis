import pandas as pd
import os
import matplotlib.pyplot as plt

from util import ReadingLogsData
from scripts import number_of_reading_log_per_student, upper_bound_threshold

GRADE_BOOK_PATH = os.path.join('data', 'processed', 'grade_book.csv')

if __name__ == '__main__':
    grade_book = pd.read_csv(GRADE_BOOK_PATH)
    data448ids = grade_book['ID'].astype('int64')
    reading_logs_data = ReadingLogsData()
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    reading_dict = reading_logs_data.get_reading_duration_dict()
    result_df, sum_rl = number_of_reading_log_per_student(module_paragraphs_dict, reading_dict, data448ids) # upper_bound_threshold(module_paragraphs_dict, reading_dict, data448ids)
    plt.hist(result_df['num_of_reading_log_submitted'].tolist(), bins=30)
    plt.title('Number of Reading Log submission Density plot')
    plt.xlabel('Number of Reading Log submission')
    plt.ylabel('Number of students')
    plt.show()
