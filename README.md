# Data 448 Analysis

## Requirements

- The latest version of Python 3

## Features

- Anonymize survey data
- Anonymize gradebook data

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

## Clustering Data

Run `python cluster_impressions.py`, to perform clustering on the Impressions of HCI Survey Data,
or `python cluster_background.py` to perform clustering on the Background Survey Data. After running either script the clustering graph will be displayed.
