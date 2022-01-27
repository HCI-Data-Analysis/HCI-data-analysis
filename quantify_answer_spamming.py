from util import ReadingLogsData
from scripts import answer_spamming

if __name__ == '__main__':
    reading_logs_data = ReadingLogsData()
    reading_dict, quiz_dict = reading_logs_data.get_parsed_reading_log_data()
    answer_spamming(quiz_dict)