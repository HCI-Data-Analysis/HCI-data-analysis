# Download Course Submission Data v1
This script will download all assignment submissions for a given course within the `https://canvas.ubc.ca` instance

## Executing
Run `python canvas_submission_retrieval.py *canvas_api_key *course_id`

## Structure
    📜 canvas_submission_retrieval.py  
     ┣ Libaray imports
     ┣ DateTimeEncoder class to convert datetime objects to string when json dumping
     ┣ Defined function: canvas_submission_retrieval()
     ┗ __name__ == "__main__"

## Structure of the Defined Function
    * canvas_submission_retrieval()
        ┣ Create Canvas instance
        ┗ For loop (course assignments):
            ┣ Open new file to write to
            ┣ Create array to store json dumps
            ┣ For loop (assignment submissions):
            ┃   ┣ Convert submission object to dict
            ┃   ┣ Remomve '_requester' from dict
            ┃   ┗ json.dumps submission dict to array
            ┗ Write array to json file
