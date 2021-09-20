# convert_survey.py

## This is a script to convert the impression of hci and background survey's into a format that removes all identifying information of the students in the class.
Removes the fields `name`. Also encodes the `id` field, anonymizing it with a key only supervisors have access to.

## Structure
📜convert_survey.py  
┣ Imports
┣ Define constant paths
┣ Defined function: convert_survey()
┗ __name__ == "__main__"

## Structure of the Defined Function
    * convert_survey()
        ┗ Get dataframe and drop the name column.
        ┗ For loop iterate over the rows in the dataframe:
            ┣ try:
            ┃   ┣ encode id
            ┃   ┃   ┗ use the encode function to convert the id to it's value in the key. Then update the dataframe with the encoded id.
            ┗ EncoderException: if the encode function does not work (the id is not in the key) remove this row from the dataframe.