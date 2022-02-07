from schemas import CourseSchema
import pandas as pd


def number_of_reading_log_per_student(module_paragraphs_dict, reading_dict, data448id):
    missing_reading_log_df = pd.DataFrame(data448id)
    missing_reading_log_df['num_of_reading_log_submitted'] = 0
    missing_reading_log_df = missing_reading_log_df.set_index('ID')

    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():

            is_valid = CourseSchema.page_is_valid(int(module_num), int(page_num))
            
            if is_valid:
                for data448id_in_rl in reading_dict[f'{module_num}-{page_num}'].index.values:
                    missing_reading_log_df.loc[int(data448id_in_rl)]['num_of_reading_log_submitted'] += 1
                    
    return missing_reading_log_df
