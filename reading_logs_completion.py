from scripts import reading_logs_completion_time

READING_TIMES = [100, 40, 45, 60, 65, 45, 60, 60, 25, 1, 25, 50]
DATA_PATH = 'data/cleaned_reading_logs'

if __name__ == "__main__":
    reading_logs_completion_time(DATA_PATH, READING_TIMES)
