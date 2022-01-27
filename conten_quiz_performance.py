from util import ReadingLogsData

if __name__ == '__main__':
    MODULE_PATH = "data/api/canvas/reading_logs/741711"
    r = ReadingLogsData()
    print(r.content_quiz_performance())
