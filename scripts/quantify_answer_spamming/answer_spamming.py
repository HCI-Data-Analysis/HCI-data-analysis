import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import math

def answer_spamming(content_quiz_dict):
    content_quiz_submit_time = []
    for reading_log_headers, pages in content_quiz_dict.items():
        for row in pages.iterrows():
            for series in row:
                if isinstance(series, pd.Series):
                    for index, elements in series.items():
                        later_time = 0
                        if index == 'time':
                            if isinstance(elements, list):
                                while len(elements) > 0:
                                    if later_time == 0:
                                        later_time = elements.pop()
                                    else:
                                        time_interval = math.floor(later_time / 1000) - math.floor(elements.pop() / 1000)
                                        content_quiz_submit_time.append(time_interval)
    #print(content_quiz_submit_time)
    
    q99, q25 = np.percentile(content_quiz_submit_time, [99 ,25])
    
    print("25 percent IQR is: " + str(q25))
    
    sns.displot(content_quiz_submit_time, binwidth=1)
    plt.xlim(0, q99)
    plt.show()
                                    