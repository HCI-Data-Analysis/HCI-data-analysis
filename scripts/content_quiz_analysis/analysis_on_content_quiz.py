import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

def content_quiz_analysis(content_quiz_dict):
    num_attempt_to_correct = {}
    for reading_log_headers, pages in content_quiz_dict.items():
        number_of_entries = 0
        num_attempt = []
        for row in pages.iterrows():
            for series in row:
                if isinstance(series, pd.Series):
                    for index, elements in series.items():
                        if isinstance(elements, str):
                            number_of_entries += 1
                            num_attempt.append(1)
                        elif isinstance(elements, list):
                            if isinstance(elements[0], str):
                                number_of_entries += 1
                                individual_attempts = 0
                                for submit in elements:
                                    if submit != 'ans':
                                        individual_attempts += 1
                                    else:
                                        individual_attempts += 1
                                        num_attempt.append(individual_attempts)
                                        break
                                    
        performance_list = [number_of_entries, num_attempt, sum(num_attempt)]
        num_attempt_to_correct[reading_log_headers] = performance_list
        #print(reading_log_headers)
    
    #  Overall content quiz attempt and  individual content quiz attemp
    overall_num_attempt = []
    individual_content_quiz_attempt = {}
    overall_content_quiz_attempt = []
    content_quiz_attempt_mean = []
    content_quiz_attempt_std = []
    content_quiz_attempt_pages = []
    for page, value in num_attempt_to_correct.items():
        if value[0] != 0:
            overall_num_attempt.extend(value[1])
            individual_content_quiz_attempt_mean = np.mean(value[1])
            individual_content_quiz_attempt_std = np.std(value[1])
            individual_content_quiz_attempt[page] = [individual_content_quiz_attempt_mean, individual_content_quiz_attempt_std]
            content_quiz_attempt_mean.append(individual_content_quiz_attempt_mean)
            content_quiz_attempt_std.append(individual_content_quiz_attempt_std)
            content_quiz_attempt_pages.append(page)
        else:
            individual_content_quiz_attempt[page] = [0, 0]
            
    overall_content_quiz_attempt.extend([np.mean(overall_num_attempt), np.std(overall_num_attempt)])
    content_quiz_attempt_mean.append(overall_content_quiz_attempt[0])
    content_quiz_attempt_std.append(overall_content_quiz_attempt[1])
    content_quiz_attempt_pages.append('Overall')
    #print(individual_content_quiz_attempt)
    #print(overall_content_quiz_attempt)
    
    fig, ax1 = plt.subplots(1)
    ax1.barh(content_quiz_attempt_pages, content_quiz_attempt_mean, xerr=content_quiz_attempt_std, capsize=3)
    ax1.set_ylabel("individual page")
    ax1.set_xlabel("Attempt")
    ax1.set_title('Mean and standard deviation of content quiz attempt')
    fig.tight_layout()
    plt.show()
    
                        

            