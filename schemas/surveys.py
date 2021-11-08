class SurveySchema:
    DATA_448_ID = 'id'
    SECTION = 'section'
    SECTION_ID = 'section_id'
    SUBMITTED = 'submitted'
    ATTEMPT = 'attempt'


class TASurveySchema:
    START_DATE = 'StartDate'
    END_DATE = 'EndDate'
    DURATION = 'Duration (in seconds)'
    FINISHED = 'Finished'
    RECORDED_DATE = 'RecordedDate'
    USER_LANGUAGE = 'UserLanguage'


class ModuleFeedbackSchema(SurveySchema):
    class Questions:
        MC_SINGLE_ANSWER = [
            'When considering the topics covered in this course so far, I would say that for most of the modules in '
            'this course, the ideal format for delivering the lecture material to me is:',

            'Considering that one lecture takes about 50 minutes scheduled class time, what was your experience with '
            'the time required to go through the content of each module? This question is about the lecture material '
            'only, and does not include the time for pre/post tests or any of the activities.',

            'Overall, I found the "Quick Review" questions at the end of each page of the lecture material helpful in '
            'making sure I understand what I read.',

            'Completing the tutorials were optional and only used to improve my pre-test score for the module. In '
            'general, I completed the tutorial activities.',

            'In general, I felt completing the tutorial activities improved my understanding of the material in the '
            'module.',

            'Overall, I felt the time it took to complete the tutorial activities was reasonable.',

            'Overall, I felt the difficulty of the tutorial activities was reasonable.',

            'In most cases, I got help during class time to complete the tutorial activities.',

            'The tutorial activities in this class were designed to be done individually. At times, I collaborated '
            'with other students but I always made sure I understood the solutions and submitted my own work for the '
            'tutorials.',

            'The tutorial activities in this class were designed to be done individually. I wish they could have been '
            'done in teams instead.',

            'In general, I felt completing the main activities improved my understanding of the material in the '
            'module more deeply than the tutorial activities or the lecture material alone. The main activities '
            'helped me appreciate the complexity of the theories, concepts, and techniques taught in the lecture '
            'material.',

            'Overall, I felt the main activities furthered my interest in HCI.',

            'Overall, I felt the time it took to complete the main activities was reasonable.',

            'Overall, I felt the difficulty of the main activities was reasonable.',

            'In most cases, I got help during class time to complete the main activities.',

            'The main activities in this class were designed to be done in teams. For the most part, we divided up '
            'the work equally. I always made sure I participated in a portion of the activity to ensure I can '
            'understand the full solution.',

            'The main activities in this class were designed to be done in teams. I wish they could have been done '
            'individually instead.',

            'Overall, I enjoy completing the main activities.',

            'In general, I felt the pre-tests were helpful in identifying what I should learn from the module content '
            'beforehand.',

            'In general, I felt that the post-tests fairly assessed whether I understand the module content.',

            'Overall, I felt the time it took to complete the pre/post-tests was reasonable.',

            'Overall, I felt the difficulty of the questions in the pre/post-tests were reasonable.',

            'Overall, I prefer having pre-tests and post-tests for each module rather than having big midterms.',

            'In general, I felt completing the project assignments improved my understanding of the material in the '
            'module more deeply than the other activities or the lecture material alone. These activities helped me '
            'appreciate the complexity of the theories, concepts, and techniques taught in the lecture material.',

            'Overall, I felt the time it took to complete each project assignment was reasonable.',

            'Overall, I felt the difficulty of the project assignments was reasonable.',

            'Overall, I enjoyed completing the project assignments.',

            'In general, I feel my performance (e.g., my grades) in the pre-tests, post-tests, tutorial activities, '
            'and main activities reflect how skillful I am in these modules.\nIn particular, if I did not do well in '
            'a module, it is mostly because I was not good at the material. On the other hand, if I did well, '
            'it was mostly because I was good at the material.',

            'In general, I feel my performance (e.g., my grades) in the pre-tests, post-tests, tutorial activities, '
            'and main activities reflect how interested I am in these modules.\nIn particular, if I did not do well '
            'in a module, it is mostly because I was not interested in the material. On the other hand, '
            'if I did well, it was mostly because I was interested in the material.',
        ]

        MC_MULTI_ANSWER = [
            'Which of the following modules did you find interesting? Check all that apply.',
        ]

        FREE_ANSWER = [
            'Are there other suggestions you\'d like to provide to help us improve the design of the modules and the '
            'associated lecture content?',

            'Any other suggestions you\'d like to provide to help us improve these modules?',
        ]
