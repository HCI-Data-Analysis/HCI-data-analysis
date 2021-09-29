# Canvas Submission Retrieval

This script will download all assignment submissions for a given course within the `https://canvas.ubc.ca` instance

Outputs a set of `.json` files equal to the amount of assignments that in the given course which containing the assignment status, submission information, marker information, and user information

There are three prarmeters that canvas_submission_retrieval() function requires - Canvas course id, Canvas access token, and export path.

1.  Canvas course id can be contained from course URL - the comination of number right after courses is the course ID:
    * Example: https://canvas.ubc.ca/courses/12345 - 12345 is the Course ID
     
2.  Canvas access token can be contained from account setting, find +New Access Token button, set up the correct expair date and give it a purpose. Afterward, Canvas will generate a token for you.
   
3.  Export path is path where you wish to store output JSON files.

    