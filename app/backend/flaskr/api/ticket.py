from flaskr.models.ticket import *
from flaskr.models.Message import *
from flaskr import database
from . import apiBluePrint
from flask import jsonify, request, escape
from flaskr import socketio
import uuid, datetime


#Make this post with a button.
@apiBluePrint.route('/ticket/<ticket_id>/close')
def close_ticket(ticket_id):
    """ Update this with a rights check."""
    ticket = Ticket.query.get(ticket_id)
    ticket.close
    db.session.commit()
    return "ticket closed"


@apiBluePrint.route('/ticket/<ticket_id>')
def retrieve_single_ticket(ticket_id):
    """
    Geeft een enkel ticket.
    """
    # TODO: Controlleer rechten
    ticketObj = Ticket.query.get(ticket_id)
    return jsonify(ticketObj.serialize)


@apiBluePrint.route('/ticket/<ticket_id>/reply', methods=['POST'])
def reply_message(ticket_id):
    """
    Tijdelijke functie, geeft altijd success terug en het bericht.
    """
    if (request.json.get("message") == ''):
        return jsonify({'status': 'failed', 'reason': 'Empty message'})
    ticket = Ticket.query.get(ticket_id)
    message = Message()
    message.ticket = ticket
    message.user_id = 12345678 # TODO: de ingelogde ta's id gebruiken
    message.text = request.json.get("message") #TODO: check voor xss
    db.session.add(message)
    db.session.commit()

    room = "ticket-messages-{}".format(ticket_id)
    socketio.emit('messageAdded', {'text': message.text, 'user_id': message.user_id}, room=room)

    try:
        database.addItemSafelyToDB(message)
    except database.DatabaseInsertException as DBerror:
        print(DBerror)
        #Need to handle this better somehow. It should never happen though.

    return jsonify({'status': "success", 'message': message.serialize})



@apiBluePrint.route('/ticket/<ticket_id>/messages')
def get_ticket_messages(ticket_id):
    """"""
    ticket = Ticket.query.get(ticket_id)
    print(database.json_list(ticket.messages))
    return database.json_list(list(ticket.messages))

# TODO: Deze verplaatsen naar user zodra die beschikbaar is
@apiBluePrint.route('/student/ticket/<ticket_id>/reply', methods=['POST'])
def student_reply_message(ticket_id):
    """
    Tijdelijke functie, geeft altijd success terug en het bericht.
    """
    if (request.json.get("message") == ''):
        return jsonify({'status': 'failed', 'reason': 'Empty message'})
    ticket = Ticket.query.get(ticket_id)
    message = Message()
    message.ticket = ticket
    message.user_id = 567 # TODO: de ingelogde ta's id gebruiken
    message.text = request.json.get("message") #TODO: check voor xss
    db.session.add(message)
    db.session.commit()

    room = "ticket-messages-{}".format(ticket_id)
    socketio.emit('messageAdded', {'text': message.text, 'user_id': message.user_id}, room=room)

    return jsonify({'status': "success", 'message': message.serialize})

@apiBluePrint.route('/ticket/submit', methods=['POST'])
def create_ticket():
    """
    Check ticket submission and add to database.
    """
    name = escape(request.json["name"])
    studentid = escape(request.json["studentid"])
    message = escape(request.json["message"])
    courseid = escape(request.json["courseid"])
    labelid = escape(request.json["labelid"])
    subject = escape(request.json["subject"])
    email = "notimplemented@nothing.nope"

    # Validate and then create the ticket.
    if ticketValidate(name, studentid, message, courseid, labelid, subject):

        ticket_new = ticket_constructor(name, studentid, message, courseid, labelid, subject, email)
        try:
            database.addItemSafelyToDB(ticket_new)
        except database.DatabaseInsertException as DBerror:
            print(DBerror)
            #Need to handle this better somehow. It should never happen though.


        return jsonify({'status': "success", 'ticketid' : str(ticket_new.id)});
    # Just return, form is invalid so a failure will occur clientside.
    return;

def ticketValidate(name, studentid, message, courseid, labelid, subject):

    # Names can only contain letters, spaces, - or ' in some cases.
    for letter in name:
        if not letter.isalpha() and not letter in " '-":
            return False

    # A number should be within certain bounds and only numerical.
    try:
        studentid_num = int(studentid)
        if studentid_num < 100000 or studentid_num > 999999999:
            return False

    except ValueError:
        return False


    if len(subject) > 50:
        return False

    # Course and labelid shoudl be valid (Implement through server checking)

    #TODO implement LTI checking for course/student accessability and validity.

    # Message should not be empty.
    if len(message) == 0:
        return False

    return True

def ticket_constructor(name, studentid, message, courseid, labelid, subject, email):

    # Create new ticket and add data.
    ticket_new = Ticket()
    ticket_new.user_id = studentid
    ticket_new.course_id = courseid #TODO get actual courseid in stead of course from form
    ticket_new.status_id = 1
    ticket_new.label_id = 1#labelid #TODO get actual label id from db instead of name.
    if len(subject) > 0:
        ticket_new.title = subject

    # TODO: Decide on string (uuid.uuid4()) or int id (current).
    ticket_new.id = uuid.uuid1().int % 9223372036854775807
    ticket_new.email = email
    ticket_new.timestamp = datetime.datetime.now()

    return ticket_new
