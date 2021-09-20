# Data 448 Anonymizer

## Requirements
 - [x] The latest version of Python 3

## Features
 - [x] Anonymize survey data
 - [x] Anonymize gradebook data
 - [x] Anonymize reading log ZIP files

## Step 1.
### Move to the terminal directory
#### Option 1 (from Finder in MacOS):
 1. Press `Command + ↑` before right-clicking the folder.
 2. Select `New Terminal at Folder` option from the list of actions
---
#### Option 2 (from Terminal):
 1. Open a terminal and `cd` to the project directory
### Install Requirements
In the terminal, install requirements using `pip install -r requirements.txt`

## Step 2.
### Run the anonymizer
In your terminal, run `python anonymizer.py` to start the application

## Step 3.
### Generate a key
Within the app, use the generate key button to upload a sample survey containing all the students, which will then download the key for you.
### Upload the key
Click the upload key to upload the previously generated file.
### Upload your files
Depending on which type of file you would like to anonymize, upload selected files according which type you would like. (The app will break if there are different files that do not have the same structure when attempting to anonymize!)