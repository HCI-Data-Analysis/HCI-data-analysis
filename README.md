# HCI-data-analysis

## Setup
We must create a file named `Key.csv` in the `/keys` directory. This csv should contain the columns (named as such):
> Name, CanvasID, StudentID, Data448ID

1. Begin with the gradebook csv, rename the columns:

        'ID' -> 'CanvasID'
        'Student Number' -> 'StudentID'
        'Student' -> 'Name'

    and delete all other columns. 
2. Re-save this version of the csv as `Key.csv` in the `/keys` directory.

`Note:` The Data448ID comprises unique 7-digit numbers in each row.
> #### Generate the Data448ID column automatically
> 1. Open `/scripts/generate_half_key.py`.
> 2. Edit `NUM_STUDENTS` to correspond to the number of students in your course.
> 3. Open a terminal in the root directory and run `python gen_half_key.py`.
> 4. A .csv will be created at `/keys/HalfKey.csv` containing 1 column for Data448ID and as many rows as you specified in step 2.
> 5. You can now open this .csv file in any spreadsheet software and copy that column into your `Key.csv` file, beside the Name, CanvasID, and StudentID columns.

## Anonymizing Data

Run `python anaonymize.py` to remove sensitive data from collected .csv files. This assumes that the .csv schemas are
properly documented in the `/schemas` directory. Currently, this includes:

- Gradebook data
- Survey data (Background survey & Impressions of HCI survey)

> #### Instructions
> 1. Place all un-anonymized .csv files in the `/raw_data` directory. (Overwrite the current .csv files in that directory)
> 2. Open `anonymize.py` and ensure that the names and file paths of each file are accurate.
> 2. Run `pip install -r requirements.txt`
> 3. Run `python anonymize.py` in your terminal.
> 4. Now you should have a `/data` directory containing the anonymized versions of the .csv files.
> - More details about the format of the resulting anonymized .csv files can be found in the related .md files in `/scripts`.