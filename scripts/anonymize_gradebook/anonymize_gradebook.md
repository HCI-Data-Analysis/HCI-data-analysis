# Anonymize Gradebook

Contains a method `anonymize_gradebook()` that uses `Key.csv` through the `Encoder` to remove all sensitive user data
and adds a generated DATA448 ID from the keys file passed into the method.

Removes student names, student IDs, SIS login IDs from the `gradebook.csv` file. Renames the ID column to `Data448ID`,
and encodes all IDs within the file to each student's corresponding Data 448 IDs.

> Note: `gradebook.csv` is an arbitrary filename and can refer to most gradebook `.csv` data exported from Canvas.

Outputs a `.csv` file containing the anonymized version of the `gradebook.csv` file. (Destination directory and filename
are parameters of the function)
