from schemas import CourseSchema
import pandas as pd


def number_of_reading_log_per_student(module_paragraphs_dict, reading_dict, data448id):
    missing_reading_log_df = pd.DataFrame(data448id)
    missing_reading_log_df['num_of_reading_log_submitted'] = 0
    missing_reading_log_df = missing_reading_log_df.set_index('ID')
    number_of_pages_valid =0

    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():

            is_valid = CourseSchema.page_is_valid(int(module_num), int(page_num))
            
            if is_valid:
                number_of_pages_valid += 1
                for data448id_in_rl in reading_dict[f'{module_num}-{page_num}'].index.values:
                    missing_reading_log_df.loc[int(data448id_in_rl)]['num_of_reading_log_submitted'] += 1
                    
    return missing_reading_log_df, number_of_pages_valid



def upper_bound_threshold(module_paragraphs_dict, reading_dict, data448id):
    # Considering there are 11 pages for mododule 0
    # School started on Jan 11st and add/drop deadliong is one Jan 22nd
    # It is only possible for people to miss module 0 and this will be used as threshold
    # Therefore they should only miss 11 mododule
    
    missing_reading_log_df, number_of_pages_valid = number_of_reading_log_per_student(module_paragraphs_dict, reading_dict, data448id)
    threshold = number_of_pages_valid - 11
    list_of_student_with_enough_reading_log_df = missing_reading_log_df[missing_reading_log_df['num_of_reading_log_submitted'] >= threshold]
    list_of_student_with_enough_reading_log = list_of_student_with_enough_reading_log_df.index.values
    
    
    return list_of_student_with_enough_reading_log