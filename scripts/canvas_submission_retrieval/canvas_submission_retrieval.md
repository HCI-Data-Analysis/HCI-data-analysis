# Canvas Submission Retrieval

This script will download all assignment submissions for a given course within the `https://canvas.ubc.ca` instance

Outputs a set of `.json` files equal to the amount of assignments that in the given course which containing the assignment status, submission information, marker information, and user information

There are three parameters that canvas_submission_retrieval() function requires - Canvas course id, Canvas access token, and export path.

1.  Canvas course id can be contained from course URL - the combination of number right after courses is the course ID:
    * Example: https://canvas.ubc.ca/courses/12345 - 12345 is the Course ID
     
2.  Canvas access token can be contained from your canvas account settings. Find the `+New Access Token` button, set up the correct expiry date and give it a purpose. Afterward, Canvas will generate a token for you which should be safely stored in a location.
   
3.  Export path is the path where you wish to store output JSON files.

To call Function canvas_submission_retrieval(). Run Following command in console:

    python canvas_submission_retrieval.py <ACCESS_TOKEN> <COURSE_ID>
