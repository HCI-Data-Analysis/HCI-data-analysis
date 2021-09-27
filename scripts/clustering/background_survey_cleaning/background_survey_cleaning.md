# Background Survey Cleaning

Contains a method called `export_to_csv()` that will take the background survey data and convert it to a csv that is
prepared for clustering. 

The questions in the background survey were all under a single column. This script moves all
the questions into their own individual columns.

The following fields were also removed to simplify the dataset with only the required data for clustering.

- `section`
- `section_id`
- `subimtted`
- `attempt`
- `Course Section`
- `Meeting Times`
- `Ideal Teammates`
- `Teammate to Avoid`
- `n correct`
- `n incorrect`
- `score`

Outputs a `.csv` to the `data` directory with the name `processed_background_survey.csv`.