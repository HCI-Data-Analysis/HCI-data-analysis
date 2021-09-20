import inspect
import os
import sys

from util import Encoder, EncoderException

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
main_dir = os.path.dirname(parent_dir)
sys.path.insert(0, main_dir)

KEY_PATH = '../../keys/Key.csv'


def convert_zip_file():
    for subdir, dirs, files in os.walk(r'../../data'):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".zip"):
                real_student_information = filename.split("_")
                try:
                    encoder = Encoder(KEY_PATH)
                    if len(real_student_information) == 3:
                        canvas_id = int(real_student_information[1])
                        half_key = encoder.encode(canvas_id)
                        id = str(half_key)
                        os.rename(filepath, '../../data/' + id + '.zip')
                    elif len(real_student_information) == 4:
                        canvas_id = int(real_student_information[1])
                        assignment_name = str(real_student_information[3])
                        half_key = encoder.encode(canvas_id)
                        id = str(half_key)
                        os.rename(filepath, '../../data/' + id + '_' + assignment_name)
                    elif len(real_student_information) == 5:
                        canvas_id = int(real_student_information[2])
                        assignment_name = str(real_student_information[4])
                        half_key = encoder.encode(canvas_id)
                        id = str(half_key)
                        os.rename(filepath, '../../data/' + id + '_' + assignment_name)
                    else:
                        print("unsuitable format")
                except EncoderException as e:
                    print(e)


if __name__ == "__main__":
    convert_zip_file()
