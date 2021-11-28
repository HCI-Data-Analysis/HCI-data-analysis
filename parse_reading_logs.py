from scripts import parse_reading_logs

MODULE_PATH = "data/api/canvas/reading_logs/741711"
MODULE_PARAGRAPHS_PATH = "data/module_paragraphs/module_paragraphs.json"

if __name__ == "__main__":
    parse_reading_logs(MODULE_PATH, MODULE_PARAGRAPHS_PATH, '0')
