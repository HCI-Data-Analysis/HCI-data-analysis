import os
import dill
from util import CACHE_FOLDER


class PreTestData:
    pre_test_first_attempt_grade_dict = None

    def get_parsed_first_attempt_grades(self) -> dict:
        if not self.pre_test_first_attempt_grade_dict:
            try:
                with open(os.path.join(CACHE_FOLDER, 'pre_test_first_attempt_grade_dict.pkl'), 'rb') as f:
                    self.pre_test_first_attempt_grade_dict = dill.load(f)
            except FileNotFoundError as e:
                raise FileNotFoundError(f'{e}\nRun "python pre_test_first_attempt_grade.py" first.')

        return self.pre_test_first_attempt_grade_dict
