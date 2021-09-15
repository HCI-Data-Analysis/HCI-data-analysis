import pandas as pd
import numpy as np

bg_survey = pd.read_csv('../../data/341_Background_Survey_Header.csv')

data448id = np.random.randint(10000, 99999, len(bg_survey.index))
bg_survey['data448id'] = data448id

bg_survey.to_csv('../../keys/keys.csv', columns=["id", "name", "section_id", "data448id"])

print(bg_survey)
