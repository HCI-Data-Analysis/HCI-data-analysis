# Data 448 Analysis
## Requirements
 - The latest version of Python 3

## Features
 - Anonymize survey data
 - Anonymize gradebook data
 - Canvas Submission Retrieval

## Anonymizing Data

Run `python anonymize.py` to remove sensitive data from collected .csv files. This assumes that the .csv schemas are
properly documented in the `/schemas` directory. Currently, this includes:

- Gradebook data
- Survey data (Background survey & Impressions of HCI survey)

> #### Instructions
> 1. Navigate to the root directory.
> 1. Place all un-anonymized .csv files in the `/raw_data` directory. (Overwrite the current .csv files in that directory)
> 2. Open `anonymize.py` and ensure that the names and file paths of each file are accurate.
> 2. Run `pip install -r requirements.txt`
> 3. Run `python anonymize.py` in your terminal.
> 4. Now you should have a `/data` directory containing the anonymized versions of the .csv files.
> - More details about the format of the resulting anonymized .csv files can be found in the related .md files in `/scripts`.

## Retrieve submission from Canvas

Run `python canvas_submission_retrieval.py <ACCESS_TOKEN> <COURSE_ID>` where `ACCESS_TOKEN` is obtained from Canvas account setting and `COURSE_ID` is obtained from Course URL. 

>#### Instruction
>1. Navigate to the root directory.
>2. Make sure Key.csv is in `/key` dicrectory.
>3. Open `submission_retrieval.py` and ensure that the names and file paths of each file are accurate.
>4. Run `pip install -r requirements.txt`
>5. Run `python canvas_submission_retrieval.py <ACCESS_TOKEN> <COURSE_ID>` and enter the correct information. 
>6. Now in `/data` dicrectory shoud have a `/canvas_submission`folder that contains a `/<COURSE_ID>` folder which stores anonymized submission information in `.json` format.
>- More details about the format of the resulting `.json` files can be found in the related `.md` files in `/scripts`.