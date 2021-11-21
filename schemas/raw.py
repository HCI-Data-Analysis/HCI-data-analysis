class RawGradeBookSchema:
    STUDENT_NAME = 'Student'
    CANVAS_ID = 'ID'
    SIS_LOGIN_ID = 'SIS Login ID'
    SECTION = 'Section'
    STUDENT_ID = 'Student Number'
    LECTURE = 'Lecture'
    LAB = 'Lab'


class RawSurveySchema:
    STUDENT_NAME = 'name'
    CANVAS_ID = 'id'
    SECTION = 'section'
    SECTION_ID = 'section_id'
    SUBMITTED = 'submitted'
    ATTEMPT = 'attempt'
    BACKGROUND_SV_FRIENDS = '3430864: Identify at most three students that you would like to be in the same team. We ' \
                            'will do our best to keep you guys together.\n\nFirst choice\n[First_choice]\n\n\nSecond ' \
                            'choice\n[Second_choice]\n\n\nThird choice\n[Third_choice]\n\n'


class RawTASurveySchema:
    START_DATE = 'StartDate'
    END_DATE = 'EndDate'
    STATUS = 'Status'
    IP_ADDRESS = 'IPAddress'
    DURATION = 'Duration (in seconds)'
    FINISHED = 'Finished'
    RECORDED_DATE = 'RecordedDate'
    RESPONSE_ID = 'ResponseId'
    RECIPIENT_LAST_NAME = 'RecipientLastName'
    RECIPIENT_FIRST_NAME = 'RecipientFirstName'
    RECIPIENT_EMAIL = 'RecipientEmail'
    EXTERNAL_REFERENCE = 'ExternalReference'
    LATITUDE = 'LocationLatitude'
    LONGITUDE = 'LocationLongitude'
    DISTRIBUTION_CHANNEL = 'DistributionChannel'
    USER_LANGUAGE = 'UserLanguage'
