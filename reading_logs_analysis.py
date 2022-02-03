from collections import defaultdict

import pandas as pd

from util import ReadingLogsData
from scripts import get_outlier_id_list, get_outlier_list_from_dataframe

MODULE_PATH = "data/api/canvas/reading_logs"
MODULE_PARAGRAPHS_PATH = "data/processed/module_paragraphs.json"

if __name__ == "__main__":

    # Outlier Categorization
    sin_dict = defaultdict(dict)
    reading_logs_data = ReadingLogsData()
    reading_log_dict = reading_logs_data.get_parsed_reading_log_data()[0]
    for item in reading_log_dict:
        sped, lag = get_outlier_id_list(reading_log_dict.get(item), item)
        for sp in sped:
            sin_dict.setdefault(sp, defaultdict(int))['SpeedRunning'] += 1

        for la in lag:
            sin_dict.setdefault(la, defaultdict(int))['Lagging'] += 1

    sin_df = pd.DataFrame.from_dict(sin_dict, orient='index')
    print(f"Outlier IDs: {get_outlier_list_from_dataframe(sin_df[['Lagging']])}")
