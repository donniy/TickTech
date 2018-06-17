from flaskr.models.ticket import *
from flaskr.models.Message import *
from flaskr.models.user import *
from flaskr import database
from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import socketio
from werkzeug.utils import secure_filename
import uuid
import datetime
from flaskr.request_processing import ticket as rp_ticket
from flaskr.request_processing import message as rp_message
from flaskr import Iresponse
from flask_jwt import jwt_required, current_identity
from flaskr.utils import notifications, course_validation, json_validation
import os


UPLOAD_FOLDER = './useruploads/'


# Make this post with a button.
@apiBluePrint.route('/ticket/<ticket_id>/close', methods=['POST', 'PATCH'])
@jwt_required()
def close_ticket(ticket_id):
    """ Update this with a rights check."""
    try:
        ticket = Ticket.query.get(ticket_id)
        ticket.close
        db.session.commit()
        notifications.notify(current_identity.id,
                             ticket,
                             'Closed ticket',
                             Message.NTFY_TYPE_CLOSED)
    except Exception as e:
        raise e
        return Iresponse.create_response(str(e), 400)
    return jsonify({'status': "success", 'message': 'ticket closed'})


@apiBluePrint.route('/ticket/<ticket_id>', methods=['GET'])
def retrieve_single_ticket(ticket_id):
    """
    Geeft een enkel ticket.
    """
    # TODO: Controlleer rechten
    ticketObj = Ticket.query.get(ticket_id)
    print(ticketObj)
    if ticketObj is None:
        print("Ticket is None")
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(ticketObj.serialize, 200)


@apiBluePrint.route('/ticket/<ticket_id>/messages', methods=['POST'])
@jwt_required()
def create_message(ticket_id):
    """
    Maak een nieuw bericht.
    """
    jsonData = request.get_json()
    if request is None:
        return Iresponse.empty_json_request()

    jsonData["user_id"] = current_identity.id

    userId = escape(jsonData["user_id"])
    msg = rp_message.create_request(jsonData, ticket_id)

    ticket = Ticket.query.get(ticket_id)
    user = User.query.get(userId)

#    if ticket is not None and user is not None:
#        # unassigned
#        if ticket.ticket_status.id == 1:
#            ticket.ticket_status = TicketStatus.query.get(4)
#        # assigned
#        elif ticket.ticket_status.id == 3:
#            ticket.ticket_status = TicketStatus.query.get(4)
#
#        tas = ticket.binded_tas
#        if user not in tas:
#            # add user to bound tas
#            tas.append(user)
#
#    db.session.commit()
    return msg


@apiBluePrint.route('/ticket/<ticket_id>/messages', methods=['GET'])
def get_ticket_messages(ticket_id):
    return rp_message.retrieve_all_request(ticket_id)


@apiBluePrint.route('/ticket/submit', methods=['POST'])
@jwt_required()
def create_ticket():
    """
    Check ticket submission and add to database.
    """

    if request.files != '':
        filecount = 0
        for file_id in request.files:
            filecount += 1
            if filecount > 5:
                return Iresponse.create_response("Too many files", 400)
            file = request.files[file_id]

            extension =  '.' + file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(str(uuid.uuid4()) + extension)
            print(filename)
            file.save(filename)
            print("SAVED")
            # size = os.stat(UPLOAD_FOLDER + filename).st_size
            # if size > MAX_SIZE:
            #   return Iresponse.create_response("File exeeds sizelimit", 400)

    message = escape(request.form['message'])
    subject = escape(request.form['subject'])
    courseid = escape(request.form['courseid'])
    labelid = escape(request.form['labelid'])
    ticket_data = {'message' :  message,
                   'subject' :  subject,
                   'courseid' :  courseid,
                   'labelid' :  labelid}

    if not course_validation.check_course_validity(courseid, labelid):
        return Iresponse.create_response("Invalid Course/Label", 400)

    ticket_data['studentid'] = current_identity.id
    ticket_data['name'] = current_identity.name
    ticket_data['email'] = current_identity.email

    if not json_validation.validate_ticket_data(ticket_data):
        return Iresponse.create_response("Invalid ticket data", 400)


    response = rp_ticket.create_request(ticket_data)

    return response
