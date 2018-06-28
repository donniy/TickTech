from . import apiBluePrint
from flaskr import database, Iresponse, plugins
from flask_jwt_extended import jwt_required
from flask import request
from flaskr.models.Label import Label, LabelPlugin
from flaskr.models.Course import Course
from flaskr.models.user import User
from flaskr.utils.json_validation import validate_json
from flaskr.auth import require_role
import uuid


@apiBluePrint.route('/labels/<label_id>/close', methods=['POST'])
@require_role(['supervisor', 'ta'])
def remove_label(label_id):
    """
    Function that removes a label.
    """
    label = Label.query.get(label_id)
    print(label)
    if label is None:
        return Iresponse.create_response("", 404)

    if not database.deleteSafelyFromDB(label, remove_label):
        return Iresponse.internal_server_error()

    return Iresponse.create_response("", 202)


@apiBluePrint.route('/labels/<course_id>', methods=['GET'])
@jwt_required
def retrieve_labels(course_id):
    """
    Returns all labels of given course.
    TODO: Controle if user has permissions.
    """
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(
        database.serialize_list(course.labels), 200)


@apiBluePrint.route('/labels/<course_id>', methods=['POST'])
@require_role(['supervisor', 'ta'])
def create_labels(course_id):
    """
    Adds a label to a course.
    """
    data = request.get_json()
    if data is None:
        return Iresponse.create_response("", 404)
    name = data["name"]
    labelid = uuid.uuid4()
    exist_label = Label.query.filter_by(label_name=name).all()

    if exist_label:
        return Iresponse.create_response("", 200)

    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)

    new_label = Label()
    new_label.label_name = name
    new_label.label_id = labelid
    new_label.course = course

    if not database.addItemSafelyToDB(new_label):
        return Iresponse.internal_server_error()

    database.db.session.commit()
    return Iresponse.create_response("", 200)


@apiBluePrint.route('/labels/<label_id>/select', methods=['POST'])
@require_role(['supervisor', 'ta'])
def selectLabel(label_id):
    """
    Select a label as teaching assistant to get notifications when new tickets
    are added with selected label.
    """
    json_data = request.get_json()

    if not validate_json(json_data, ["user_id"]):
        return Iresponse.create_response("", 404)

    user_id = json_data["user_id"]
    user = User.query.get(user_id)
    label = Label.query.get(label_id)
    user.labels.append(label)
    database.db.session.add(user)
    database.db.session.commit()
    return Iresponse.create_response("", 200)


@apiBluePrint.route('/labels/<label_id>/deselect', methods=['POST'])
@require_role(['supervisor', 'ta'])
def deselectLabel(label_id):
    """
    Remove label selected as teaching assistant.
    """
    json_data = request.get_json()

    if not validate_json(json_data, ["user_id"]):
        return Iresponse.create_response("", 404)

    user_id = json_data["user_id"]
    user = User.query.get(user_id)
    label = Label.query.get(label_id)
    user.labels.remove(label)
    database.db.session.add(user)
    database.db.session.commit()
    return Iresponse.create_response("", 200)


@apiBluePrint.route('/labels/<label_id>/plugins', methods=['GET'])
def get_plugins(label_id):
    """
    Retrieve all available plugins for this label, along with the active state
    and assignment id.
    """
    # TODO: Check if user is supervisor in this label's course.
    label = Label.query.get_or_404(label_id)
    return Iresponse.create_response(label.get_plugins(), 200)


@apiBluePrint.route('/labels/<label_id>/plugins', methods=['POST'])
def activate_plugin(label_id):
    """
    Create a record in the database to activate this plugin.
    """
    # TODO: Check if user is supervisor in this label's course.
    label = Label.query.get_or_404(label_id)
    plugin_id = request.get_json()['plugin_id']
    if plugin_id not in plugins.plugin_list():
        return Iresponse.create_response({"error": "Plugin does not exist"},
                                         404)
    lp = LabelPlugin()
    lp.id = uuid.uuid4()
    lp.plugin = plugin_id
    lp.label = label
    lp.assignment_id = ''
    if database.addItemSafelyToDB(lp):
        return Iresponse.create_response({"status": "success"}, 200)
    else:
        return Iresponse.create_response({"error": "Something went wrong"},
                                         500)


@apiBluePrint.route('/labels/<label_id>/plugins/<plugin_id>', methods=['PUT'])
def update_plugin(label_id, plugin_id):
    """
    Change the assignment id of this plugin for this label.
    """
    # TODO: Check if user is supervisor in this label's course.
    label = Label.query.get_or_404(label_id)
    plugin = label.get_plugin(plugin_id)
    if not plugin:
        return Iresponse.create_response({"error": "plugin not found"}, 200)
    plugin.assignment_id = request.get_json()['assignment_id']
    try:
        db = database.get_db()
        db.session.commit()
        return Iresponse.create_response({"status": "success"}, 200)
    except Exception as e:
        print(e)
        return Iresponse.create_response({"status": "failure"}, 500)


@apiBluePrint.route('/labels/<label_id>/plugins/<plugin_id>',
                    methods=['DELETE'])
def deactivate_plugin(label_id, plugin_id):
    """
    Remove this plugin-label combination from the database to deactivate it.
    Note that dis also removes the assignment id which is stored in the
    pivot table.
    """
    # TODO: Check if user is supervisor in this label's course.
    label = Label.query.get_or_404(label_id)
    plugin = label.get_plugin(plugin_id)
    if not plugin:
        return Iresponse.create_response({"error": "plugin not found"}, 200)

    try:
        db = database.get_db()
        db.session.delete(plugin)
        db.session.commit()
        return Iresponse.create_response({"status": "success"}, 200)
    except Exception as e:
        print(e)
        return Iresponse.create_response({"status": "failure"}, 500)


@apiBluePrint.route('/labels/<label_id>/selected', methods=['POST'])
@require_role(['supervisor', 'ta'])
def labelSelected(label_id):
    """
    Return a boolean for selected labels.
    """
    json_data = request.get_json()

    if not validate_json(json_data, ["user_id"]):
        return Iresponse.create_response("", 404)

    user_id = json_data["user_id"]
    user = User.query.get(user_id)
    label = Label.query.get(label_id)
    return Iresponse.create_response({'bool': label in user.labels}, 200)
