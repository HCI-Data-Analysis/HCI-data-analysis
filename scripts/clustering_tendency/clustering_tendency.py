#import the packages
import pandas as pd # working with data
from pyclustertend import vat
from pyclustertend import ivat
from pyclustertend import hopkins

def clustering_tendency(DATA_PATH_impression, DATA_PATH_BACKGROUND):
    df_impression_survey = pd.read_csv(DATA_PATH_impression)
    df_background_survey = pd.read_csv(DATA_PATH_BACKGROUND)
    
    background_survey_trim = df_background_survey.drop(columns=['id'], axis=1)
    background_survey_array = background_survey_trim.values
    impression_survey_trim = df_impression_survey.drop(columns=['id'], axis=1)
    impression_survey_array = impression_survey_trim.values
    
    background_survey_hopkins = hopkins(background_survey_array, 90)
    impression_survey_hopkins = hopkins(impression_survey_array, 90)
    
    ivat(background_survey_array)
    ivat(impression_survey_array)
    
    vat(background_survey_array)
    vat(impression_survey_array)
    
    print("Background Survey hopkins statstics: " + str(background_survey_hopkins))
    print("Impression Survey hopkins statstics: " + str(impression_survey_hopkins))
    
    
    
if __name__ == "__main__":
    clustering_tendency('for_clustering_impression_survey1.csv', 'for_clustering_processed_background_survey.csv')
    
    