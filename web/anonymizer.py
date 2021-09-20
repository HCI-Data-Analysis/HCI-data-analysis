import eel
from utils.decodeBase64 import generate_decoded_file


eel.expose(generate_decoded_file)


def init_eel():
    eel.init('anonymizer')
    eel.start('main.html')


if __name__ == '__main__':
    init_eel()
