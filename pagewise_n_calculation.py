import os
from collections import defaultdict

import pandas as pd

from util import ReadingLogsData

if __name__ == "__main__":
    count_dict = defaultdict(dict)
    reading_logs_data = ReadingLogsData()
    reading_log_dict = reading_logs_data.get_parsed_reading_log_data()[0]
    for item in reading_log_dict:
        page_df = reading_log_dict.get(item)
        count_dict[item] = page_df.shape[0]  # get the number of rows
        pd.DataFrame.from_dict(count_dict, orient='index').to_csv(os.path.join('data', 'count_dict.csv'))
