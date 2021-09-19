import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
maindir = os.path.dirname(parentdir)
sys.path.insert(0, maindir)

from util import *

KEY_PATH = '../../keys/Key.csv'

def convert_zip_file():
    for subdir, dirs, files in os.walk(r'../../data'):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".zip"):
                real_student_information = filename.split("_")
                try:
                    encoder = Encoder(KEY_PATH)
                    if (len(real_student_information) == 3):
                        canvas_id = int(real_student_information[1])
                        half_key = encoder.encode(canvas_id)
                        id = str(half_key)
                        os.rename(filepath,'../../data/' + id +'.zip')
                    elif (len(real_student_information) == 4):
                        canvas_id = int(real_student_information[1])
                        assignment_name = str(real_student_information[3])
                        half_key = encoder.encode(canvas_id)
                        id = str(half_key)
                        os.rename(filepath,'../../data/' + id + '_' + assignment_name)
                    elif (len(real_student_information) == 5):
                        canvas_id = int(real_student_information[2])
                        assignment_name = str(real_student_information[4])
                        half_key = encoder.encode(canvas_id)
                        id = str(half_key)
                        os.rename(filepath,'../../data/' + id + '_' + assignment_name)
                    else:
                        print("unsuitable format")
                except EncoderException as e:
                    print(e)

if __name__ == "__main__":
    convert_zip_file()

