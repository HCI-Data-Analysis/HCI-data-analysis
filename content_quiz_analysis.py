from util import ReadingLogsData
from scripts import content_quiz_attempts_analysis, content_quiz_grade_analysis

if __name__ == '__main__':
    reading_logs_data = ReadingLogsData()
    reading_dict, quiz_dict = reading_logs_data.get_parsed_reading_log_data()
    # content_quiz_attempts_analysis(quiz_dict)
    content_quiz_grade_analysis(quiz_dict)