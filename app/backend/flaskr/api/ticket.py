from flaskr.models.ticket import Ticket
from flaskr.models.Message import Message
from flaskr.models.user import User
from . import apiBluePrint
import uuid
import datetime
from flask_jwt_extended import jwt_required
from flaskr.jwt_wrapper import get_current_user
from flask import request, escape, jsonify, current_app
from flaskr import plugins
from flaskr.request_processing import ticket as rp_ticket
from flaskr.request_processing import message as rp_message
from flaskr.request_processing import file as rp_file
from flaskr import Iresponse
from flaskr.utils import notifications
from flask_mail import Mail
from mail.Message import createEmailMessage
from flaskr.utils import course_validation, json_validation, ocr
from os.path import expanduser
import base64
import mimetypes
from flaskr import database
from threading import Thread
from flask import current_app
from flaskr.auth import require_role


@apiBluePrint.route('/ticket/<ticket_id>/close', methods=['POST', 'PATCH'])
@jwt_required
def close_ticket(ticket_id):
    """
    Close ticket when is has been handled.
    TODO: Update this with a rights check.
    """
    current_identity = get_current_user()
    try:
        ticket = Ticket.query.get(ticket_id)
        ticket.close
        database.db.session.commit()
        notifications.notify(current_identity.id,
                             ticket,
                             'Closed ticket',
                             Message.NTFY_TYPE_CLOSED)
    except Exception as e:
        print(e)  # LOGGING
        return Iresponse.create_response("Error", 400)
    # TODO: Add Iresponse.
    return jsonify({'status': "success", 'message': 'ticket closed'})


@apiBluePrint.route('/ticket/<ticket_id>', methods=['GET'])
@jwt_required
def retrieve_single_ticket(ticket_id):
    """
    Retrieve single ticket from database.
    """
    # TODO: Controlleer rechten
    ticketObj = Ticket.query.get(ticket_id)
    if ticketObj is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(ticketObj.serialize, 200)


@apiBluePrint.route('/ticket/<ticket_id>/plugins', methods=['GET'])
@require_role(['ta', 'supervisor'])
def retrieve_plugins(ticket_id):
    """
    List the plugins available for this ticket.
    """
    print("===Retrieving plugins for ticket===")
    ticketObj = Ticket.query.get_or_404(ticket_id)
    # TODO: For now this returns all available plugins.
    pls = {}
    for p in plugins.plugin_list():
        pl = plugins.get_plugin(p)
        pls[pl.display_name] = pl.get_assignment_info(ticketObj.owner.id, 123)
    return Iresponse.create_response(pls, 200)


@apiBluePrint.route('/ticket/<ticket_id>/messages', methods=['POST'])
@jwt_required
def create_message(ticket_id):
    """
    Create a new message.
    """
    json_data = request.get_json()
    if request is None:
        return Iresponse.empty_json_request()

    current_identity = get_current_user()
    json_data["studentid"] = current_identity.id

    userId = escape(json_data["studentid"])
    msg = rp_message.create_request(json_data, ticket_id)

    ticket = Ticket.query.get(ticket_id)
    user = User.query.get(userId)

    if(ticket.user_id != user.id):
        message = createEmailMessage(ticket.title,
                                     [ticket.email], ticket_id,
                                     json_data['message'], user.name)
        if current_app.config['SEND_MAIL_ON_MESSAGE']:
            print("send email")
            app = current_app._get_current_object()
            thr = Thread(target=send_async_email, args=[message, app])
            thr.start()
    return msg


def send_async_email(message, app):
    with app.app_context():
        print("SENDED EMAIL")
        res = Mail().send(message)
        print(res)


@apiBluePrint.route('/ticket/<ticket_id>/messages', methods=['GET'])
@jwt_required
def get_ticket_messages(ticket_id):
    """
    Retrieve messages in ticket.
    TODO: Check if user is related to ticket.
    """
    return rp_message.retrieve_all_request(ticket_id,
                                           get_current_user(),
                                           read=True)


@apiBluePrint.route('ticket/addta', methods=['POST'])
@require_role(['ta', 'supervisor'])
def add_ta_to_ticket():
    """
    Assign teaching assistant to ticket.
    """
    json_data = request.get_json()
    if json_data:
        if json_validation.validate_json(json_data, ['taid', 'ticketid']):
            return rp_ticket.add_ta_to_ticket(json_data)
    return Iresponse.create_response("Invalid request", 400)


@apiBluePrint.route('ticket/removeta', methods=['POST'])
@require_role(['ta', 'supervisor'])
def remove_ta_from_ticket():
    """
    Unassign teaching assistant from ticket.
    """
    json_data = request.get_json()
    if json_data:
        if json_validation.validate_json(json_data, ['taid', 'ticketid']):
            return rp_ticket.remove_ta_from_ticket(json_data)
    return Iresponse.create_response("Invalid request", 400)


@apiBluePrint.route('/ticket/submit', methods=['POST'])
@require_role(['student'])
def create_ticket():
    """
    Check ticket submission and add to database.
    """
    print(request.headers)
    # Mandatory check to comply with incompatible testing.
    formdata = None
    if request.get_json():
        data = request.get_json()
        formdata = {'subject': data['subject'],
                    'message': data['message'],
                    'courseid': data['courseid'],
                    'labelid': data['labelid'],
                    }
    else:
        formdata = request.form

    if hasattr(request, 'files'):
        if request.files != '':
            filecount = 0
            file_names = list()
            for file_id in request.files:
                filecount += 1
                if filecount > 5:
                    return Iresponse.create_response("Too many files", 400)
                file = request.files[file_id]

                if not rp_file.save_file(file, file_names):
                    print("invalid file")
                    return Iresponse.create_response("File too large", 400)

    if not json_validation.validate_json(formdata, ['message',
                                                    'subject',
                                                    'courseid',
                                                    'labelid']):
        return Iresponse.create_response("Malformed request", 400)

    message = escape(formdata['message'])
    subject = escape(formdata['subject'])
    courseid = escape(formdata['courseid'])
    labelid = escape(formdata['labelid'])
    ticket_data = {'message':  message,
                   'subject':  subject,
                   'courseid':  courseid,
                   'labelid':  labelid,
                   'files': file_names}

    if not course_validation.check_course_validity(courseid, labelid):
        for file in file_names:
            rp_file.remove_file(file)
        return Iresponse.create_response("Invalid Course/Label", 400)

    current_identity = get_current_user()

    ticket_data['studentid'] = current_identity.id
    ticket_data['name'] = current_identity.name
    ticket_data['email'] = current_identity.email

    if not json_validation.validate_ticket_data(ticket_data):
        for file in file_names:
            rp_file.remove_file(file)
        return Iresponse.create_response("Invalid ticket data", 400)

    response = rp_ticket.create_request(ticket_data)

    return response


@apiBluePrint.route('/ticket/filedownload', methods=['POST'])
@jwt_required
def download_file():
    """
    Download a file from server (check rights in future).
    """
    json_data = request.get_json()
    if 'address' in json_data:
        homefolder = expanduser("~")
        base = '/serverdata/'
        location = json_data['address'].rsplit('/', 1)[0]
        folder = homefolder + base + location
        file = json_data['address'].rsplit('/', 1)[1]
        full_path = folder + json_data['address']

        fileType, fileEncoding = mimetypes.guess_type(full_path)

        if folder and file:
            fp = open(folder + '/' + file, 'br').read()
            encoded = base64.b64encode(fp).decode("utf-8")
            return Iresponse.create_response({'encstring': str(encoded),
                                             'mimetype': fileType}, 200)
    else:
        return Iresponse.create_response("No address", 404)


@apiBluePrint.route('/ticket/gettext', methods=["POST"])
@jwt_required
def get_text():
    """
    Convert an image file to text using Optical character recognition.
    """
    try:
        json_data = request.get_json()
        if 'address' in json_data:
            homefolder = expanduser("~")
            base = '/serverdata/'
            location = homefolder + base + json_data['address']
            text = ocr.ocr_process_image(location)
            if text:
                return Iresponse.create_response(text, 200)
            else:
                return Iresponse.create_response("Bad request", 400)
    except IOError:
        return Iresponse.create_response("Bad request", 400)
