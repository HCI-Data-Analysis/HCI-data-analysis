from collections import defaultdict

import pandas as pd


from scripts import parse_reading_logs_all, get_outlier_id_list

MODULE_PATH = "data/api/canvas/reading_logs"
MODULE_PARAGRAPHS_PATH = "data/processed/module_paragraphs.json"

if __name__ == "__main__":
    sin_dict = defaultdict(dict)
    reading_log_dict, quiz_dict = parse_reading_logs_all(MODULE_PATH, MODULE_PARAGRAPHS_PATH)
    for item in reading_log_dict:
        sped, lag = get_outlier_id_list(reading_log_dict.get(item), item)
        for sp in sped:
            sin_dict.setdefault(sp, defaultdict(int))['SpeedRunning'] += 1

        for la in lag:
            sin_dict.setdefault(la, defaultdict(int))['Lagging'] += 1

    sin_df = pd.DataFrame.from_dict(sin_dict, orient='index')
