# Anonymize TA Survey

Contains a method `anonymize_ta_survey()` that uses `Key.csv` through the `Encoder` to remove all sensitive user data
and adds a generated DATA448 ID from the keys file passed into the method.

Removes the following fields from the `ta_survey.csv` file:

- IP Address
- Status
- Response ID
- Recipient First Name
- Recipient Last Name
- Recipient Email
- External Reference
- Latitude
- Longitude
- Distribution Channel

> Note: `ta_survey.csv` is an arbitrary filename.

Outputs a `.csv` file containing the anonymized version of the `ta_survey.csv` file. (Destination directory and filename
are parameters of the function)