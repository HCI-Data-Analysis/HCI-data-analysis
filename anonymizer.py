import eel
import os
import shutil
from scripts.utils.decodeBase64 import generate_decoded_file
from scripts.key_generator.key_generator import generate_key
from scripts.survey_anonymizers.survey_anonymizer import survey_anonymize
from scripts.zip_file_anonymizer.zip_file_anonymizer import zip_anonymize
from scripts.gradebook_anonymizers.gradebook_anonymizer import gradebook_anonymize


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
