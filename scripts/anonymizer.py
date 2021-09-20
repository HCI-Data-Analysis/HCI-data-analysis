import eel
from utils.decodeBase64 import generate_decoded_file
from scripts.key_generator.key_generator import generate_key
from scripts.survey_anonymizers.survey_anonymizer import survey_anonymize
from scripts.zip_file_anonymizer.zip_file_anonymizer import zip_anonymize


eel.expose(generate_decoded_file)
eel.expose(generate_key)
eel.expose(survey_anonymize)
eel.expose(zip_anonymize)


def start_eel():
    eel.init('web/anonymizer')
    eel.start('main.html')


if __name__ == '__main__':
    start_eel()
    print('closing')
