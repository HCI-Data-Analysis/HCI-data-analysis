# Data 448 Analysis

## Requirements

- The latest version of Python 3

## Features

- Anonymize survey data
- Anonymize gradebook data
- Canvas Submission Retrieval

## Environment File Setup

```
CANVAS_ACCESS_TOKEN=
CANVAS_COURSE_ID=
```

> Information on how to retrieve these values can be found in [this guide](scripts/canvas_submission_retrieval/canvas_submission_retrieval.md).

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
or `python cluster_background.py` to perform clustering on the Background Survey Data. After running either script the
clustering graph will be displayed.

## Retrieve submission from Canvas

Run `python canvas_submission_retrieval.py <ACCESS_TOKEN> <COURSE_ID>` where `ACCESS_TOKEN` is obtained from Canvas
account setting and `COURSE_ID` is obtained from Course URL.

## Determine Average KMeans Iterations

> #### Instructions
> 1. Navigate to the root directory.
> 2. Open `average_kmeans_iterations.py` and ensure that the names and file paths of each file are accurate. You can also update the number of iterations you want to determine the average for.
> 3. Run `pip install -r requirements.txt`.
> 4. Run `python average_kmeans_iterations` and the average iterations for convergence will be printed to the terminal.

> #### Instruction
> 1. Navigate to the root directory.
> 2. Make sure Key.csv is in `/key` directory.
> 3. Open `submission_retrieval.py` and ensure that the names and file paths of each file are accurate.
> 4. Run `pip install -r requirements.txt`
> 5. Run `python canvas_submission_retrieval.py <ACCESS_TOKEN> <COURSE_ID>` and enter the correct information.
> 6. Now in `/data` directory should have a `/canvas_submission`folder that contains a `/<COURSE_ID>` folder which stores anonymized submission information in `.json` format.
> - More details about the format of the resulting `.json` files can be found in the related `.md` files in `/scripts`.