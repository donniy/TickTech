from . import apiBluePrint
from flaskr import jsonify
from flaskr.models.user import *
from flaskr import database

# remember to add file in __init__
@apiBluePrint.route('/courses/<user_id>')
def retrieve_courses(user_id):
    # TODO get courses from LTI api
    # TODO put user id in data and not in link

    user = User.query.get(user_id)
    courses = user.ta_courses
    return database.json_list(courses)
