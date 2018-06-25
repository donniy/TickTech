from flaskr.request_processing import courses
import re
import uuid


def check_course_validity(courseid, labelid):

    # Check if the ids are valid uuids (to prevent a 500 crash)
    regex = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}"
                       r"-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

    if not courseid:
        return False
    elif not regex.match(courseid):
        return False

    course = courses.single_course_request(courseid)

    if course and len(labelid) < 1:
        return True
    if course and len(labelid) > 1:
        for label in course.labels:
            if uuid.UUID(labelid) == label.label_id:
                return True
    return False
