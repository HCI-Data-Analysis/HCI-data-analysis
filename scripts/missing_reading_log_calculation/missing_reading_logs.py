from schemas import CourseSchema
import pandas as pd
import matplotlib as plt

def number_of_reading_log_per_student(module_paragraphs_dict, reading_dict, data448id):
    missing_reading_log_df = pd.DataFrame(data448id)
    missing_reading_log_df['num_of_reading_log_submitted'] = 0
    missing_reading_log_df = missing_reading_log_df.set_index('ID')
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            cs = CourseSchema()
            isValid = cs.page_is_valid(int(module_num), int(page_num))
            
            if isValid:
                for data448id_in_rl in (reading_dict[f'{module_num}-{page_num}'].index.values):
                    missing_reading_log_df.loc[int(data448id_in_rl)].values[0] = missing_reading_log_df.loc[int(data448id_in_rl)].values[0] + 1
                    
    print(missing_reading_log_df)
                    
    return missing_reading_log_df