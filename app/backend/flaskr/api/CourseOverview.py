from . import apiBluePrint
from flaskr import jsonify


# remember to add file in __init__
@apiBluePrint.route('/courses')
def retrieve_courses():
    # TODO get courses from LTI api
    courses = [{
        "id":1,
        "name":"Project Software Engineering",
        "description":"short description of course",
        "link":"/project_software_engineering"  #dit kan denk ik met id en /course/:id ofzo
    },{
        "id":2,
        "name":"Operating systems",
        "description":"short description of course",
        "link":"/operating_systems" #dit kan denk ik met id en /course/:id ofzo
    }]
    return jsonify(courses)
