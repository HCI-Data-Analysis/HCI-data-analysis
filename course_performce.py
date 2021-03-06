import pandas as pd

from scripts.course_performace_analysis.course_performace_analysis import course_performance_analysis

GRADEBOOK_PATH = 'data/anonymized/grade_book.csv'
QUIZSCOREJSON_PATH = 'data/anonymized/quizzes'
QUIZ_OBJECT_PATH = 'data/api/canvas/quiz_objects'

if __name__ == '__main__':
    gradebook = pd.read_csv(GRADEBOOK_PATH)
    course_performance_analysis(gradebook, QUIZSCOREJSON_PATH, QUIZ_OBJECT_PATH)
