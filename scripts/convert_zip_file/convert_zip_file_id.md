# convert_zip_file_id.py

## This is a script that will interate through files in data folder, find all file end with .zip and change the name ofthe zip file with the DATA448ID we generated before using encoder function.

## Structure
📜convert_zip_file_id.py  
┣ Libaray imports
┣ mimic PYTHONPATH using sys.path so python recognize util folder and Encoder class(read note 1)
┣ KEY_PATH for encoder defined
┣ Defined function: convert_zip_file()
┗ __name__ == "__main__"

## Structure of the Defined Function
    * convert_zip_file()
        ┗ For loop (data folder):
            ┣ Find any file with.zip in filename and extract real student information out of it. filename is split by _
            ┣ try:
            ┃   ┣ if(size of the extract information list is 3):
            ┃   ┃   ┗change zip file name(name_canvasid_number.zip) to DATA488ID.zip(this is reading log zip file)
            ┃   ┣ else if(size of the extract information list is 4):
            ┃   ┃   ┗change zip file name(name_canvasid_number_assignment.zip) to DATA488ID_assignment.zip(this is assignment zip file)
            ┃   ┣ else if(size of the extract information list is 5):
            ┃   ┃   ┗change zip file name(name_LATE_canvasid_number_assignemt.zip) to DATA488ID_assignment.zip(this is assignment zip file but late)
            ┃   ┗ else print this file is not in suitable format
            ┗ EncoderException: if any problem of encoder, the program does not break and give us the error for debug
## Note
    * 1. Starting from Python 3.3, implicit relative references are allowed no more. Therefore, from util import Encoder is not possible unless PYTHONPATH(an environment variable which contains the list of packages that will be loaded by Python upon execution) is set up. However, it require use command line. For the usability of the code. I use sys.path to mimic PYTHONPATH to perform the same thing.
