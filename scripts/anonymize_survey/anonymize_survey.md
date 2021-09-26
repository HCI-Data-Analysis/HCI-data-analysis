# Anonymize Survey

Contains a method `anonymize_survey()` that uses `Key.csv` through the `Encoder` to remove all sensitive user data
and adds a generated DATA448 ID from the keys file passed into the method.

Removes student names from the `survey.csv` file. Renames the ID column to `Data448ID`, and encodes all IDs within the 
file to each student's corresponding Data 448 IDs.
> Note: `survey.csv` is an arbitrary filename and can refer to most `.csv` data exported from Canvas.

Outputs a `.csv` file containing the anonymized version of the `survey.csv` file. (Destination directory and filename
are parameters of the function)

