import pandas as pd

from scripts import analyze_module_feedback, compare_module_feedback

MODULE_FEEDBACK_SURVEY_1_PATH = 'data/anonymized/ModuleFeedback1.csv'
MODULE_FEEDBACK_SURVEY_2_PATH = 'data/anonymized/ModuleFeedback2.csv'

if __name__ == '__main__':
    module_feedback_survey_1_df = pd.read_csv(MODULE_FEEDBACK_SURVEY_1_PATH)
    module_feedback_survey_2_df = pd.read_csv(MODULE_FEEDBACK_SURVEY_2_PATH)
    # analyze_module_feedback(module_feedback_survey_1_df)
    compare_module_feedback(module_feedback_survey_1_df, module_feedback_survey_2_df)
