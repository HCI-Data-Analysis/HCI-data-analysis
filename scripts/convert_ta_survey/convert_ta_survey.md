# convert_ta_survey.py

## This is a script to convert the TA survey into a format that removes all identifying information of the TAs in the class.

## Structure
📜convert_ta_survey.py  
┣ Imports
┣ Define constant paths
┣ Defined function: convert_survey()
┗ __name__ == "__main__"

## Structure of the Defined Function
    * convert_ta_survey()
        ┗ Get dataframe and drop all identifying columns.
        ┗ Return the dataframe.