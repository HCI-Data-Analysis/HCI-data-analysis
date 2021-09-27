import os
import shutil

import eel

from scripts.anonymize_gradebook.anonymize_gradebook import gradebook_anonymize
from scripts.generate_key.generate_key import generate_key
from scripts.anonymize_survey.anonymize_survey import survey_anonymize
from scripts.anonymize_zip_file.anonymize_zip_file import zip_anonymize
from util.decode_base_64 import generate_decoded_file

eel.expose(generate_decoded_file)
eel.expose(generate_key)
eel.expose(survey_anonymize)
eel.expose(zip_anonymize)
eel.expose(gradebook_anonymize)


def close_callback(route, websockets):
    if not websockets:
        shutil.rmtree('web/anonymizer/anonymized')
        os.makedirs('web/anonymizer/anonymized')
        shutil.rmtree('web/anonymizer/key')
        os.mkdir('web/anonymizer/key')
        shutil.rmtree('web/anonymizer/temp')
        os.mkdir('web/anonymizer/temp')
        os.mkdir('web/anonymizer/temp/key')
        exit()


def start_eel():
    eel.init('web/anonymizer')
    eel.start('main.html', close_callback=close_callback)


if __name__ == '__main__':
    start_eel()
