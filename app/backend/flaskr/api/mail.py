from . import apiBluePrint
from flask import escape, request, current_app
from flask_mail import Mail
from flaskr import Iresponse, database
from flaskr.models.Course import Course
from flaskr.models.user import User
from flaskr.models.ticket import Ticket
from flaskr.request_processing import ticket as rp_ticket
from flaskr.request_processing import file as rp_file
from flaskr.request_processing import message as rp_message
from flaskr.utils import course_validation, json_validation
from flaskr.utils.json_validation import validate_json
from mail.Message import ticketErrorEmail, createdEmailMessage
from mail.Message import somethingWentWrong, replyErrorEmail
from mail.Message import createdTicketEmail
from mail.thread import MailThread
from threading import Thread
import base64


def sendAsyncEmail(message, app):
    '''
    Helper function to send an email when a message has been added to a ticket.
    '''
    with app.app_context():
        Mail().send(message)


@apiBluePrint.route('/email/user/match/email', methods=['POST'])
def mailMatchWithEmail():
    '''
    Try to match incoming email to an email address.
    '''
    # Request and check the data.
    json_data = request.get_json()
    if not validate_json(json_data, ['email']):
        return Iresponse.empty_json_request()

    # Match on first success.
    email = json_data['email'].lower()
    user = User.query.filter_by(email=email).first()

    if user is not None:
        id = user.id
        success = True
    else:
        id = None
        success = False
    response = {
        'success': success,
        'studentid': id
    }
    return Iresponse.create_response(response, 200)


@apiBluePrint.route('/email/user/match/studentid', methods=['POST'])
def mailMatchWithStudentID():
    '''
    Try to match incomming email on studentid.
    '''
    # Request and check the data.
    json_data = request.get_json()
    if not validate_json(json_data, ['studentid']):
        return Iresponse.empty_json_request()

    # Match on first success.
    studentid = json_data['studentid']
    user = User.query.filter_by(id=studentid).first()

    if user is not None:
        id = user.id
        success = True
    else:
        id = None
        success = False
    response = {
        'success': success,
        'studentid': id
    }

    return Iresponse.create_response(response, 200)


@apiBluePrint.route('/email/user/match/failed', methods=['POST'])
def mailNotifyFailedMatch():
    '''
    Notify user that an email failed to match.
    '''
    # Request and check the data.
    json_data = request.get_json()
    if not validate_json(json_data, ['body', 'subject', 'address']):
        return Iresponse.empty_json_request()

    # Match on first success.
    subject = json_data['subject']
    address = json_data['address']
    body = json_data['body']
    subject = subject.replace('\n', '')
    message = ticketErrorEmail(subject, [address], body)
    app = current_app._get_current_object()
    thr = Thread(target=sendAsyncEmail, args=[message, app])
    thr.start()

    return Iresponse.create_response('Success', 200)


@apiBluePrint.route('/email/ticket/submit', methods=['POST'])
def createEmailTicket():
    '''
    Check a ticket submission and add it to database.
    '''
    # Mandatory check to comply with incompatible testing.
    formdata = request.get_json()
    files = formdata['files']

    # Check if there are too many files.
    if (len(files.keys()) > 5):
        somethingWentWrongMessage(formdata['subject'],
                                  formdata['email'],
                                  'Ticket: Too many files',
                                  formdata['message'])
        return Iresponse.create_response('Too many files', 400)

    filenames = list()
    # Check if files are the right size.
    for filename in files.keys():
        file = base64.b64decode(files[filename])

        if not rp_file.save_file_from_mail(file, filename, filenames):
            somethingWentWrongMessage(formdata['subject'],
                                      formdata['email'],
                                      'Ticket: File too large.',
                                      formdata['message'])
            return Iresponse.create_response('File too large', 400)
    formdata['files'] = filenames

    # Check if all data resulted in a valid json.
    if not json_validation.validate_json(formdata, ['message',
                                                    'subject',
                                                    'courseid',
                                                    'labelid']):
        somethingWentWrongMessage(formdata['subject'],
                                  formdata['email'],
                                  'Ticket: validate json data.',
                                  formdata['message'])
        return Iresponse.create_response('Malformed request', 400)

    # Check if the course is valid.
    if not course_validation.check_course_validity(formdata['courseid'],
                                                   formdata['labelid']):
        for file in filenames:
            rp_file.remove_file(file)
        return Iresponse.create_response('Invalid Course/Label', 400)

    # Check if uploading the files went succesful.
    if not json_validation.validate_ticket_data(formdata):
        for file in filenames:
            rp_file.remove_file(file)
        somethingWentWrongMessage(formdata['subject'],
                                  formdata['email'],
                                  'Ticket: validate ticket data.',
                                  formdata['message'])
        return Iresponse.create_response('Invalid ticket data', 400)

    response = rp_ticket.create_request(formdata)

    # Send an email to the student to confirm we received the ticket.
    if (response.status_code == 201):
        ticketid = response.get_json()['json_data']['ticketid']
        message = createdTicketEmail(formdata['subject'],
                                     [formdata['email']],
                                     ticketid,
                                     formdata['message'])
        app = current_app._get_current_object()
        thr = Thread(target=sendAsyncEmail, args=[message, app])
        thr.start()
    return response


@apiBluePrint.route('/email/ticket/newmessage', methods=['POST'])
def createEmailMessage():
    '''
    Add a message to an existing ticket.
    '''
    formdata = request.get_json()
    # Check if the ticket and message have a valid JSON.
    if not json_validation.validate_json(formdata, ['ticketid']):
        somethingWentWrongMessage(formdata['subject'],
                                  formdata['email'],
                                  'Message: validate json data.',
                                  formdata['message'])
        return Iresponse.create_response('Malformed request', 400)

    ticket = Ticket.query.get(formdata['ticketid'])

    # Check if the ticket related to the message is valid.
    if ticket is None:
        somethingWentWrongMessage(
            formdata['subject'],
            formdata['email'],
            'Message: Could not find a ticket with that id.',
            formdata['message'])
        return Iresponse.create_response('Could not find ticket', 400)

    formdata['studentid'] = ticket.user_id
    msg = rp_message.create_request(formdata, formdata['ticketid'])

    # Send an email to the student to notify them of our failing in life.
    if (msg.status_code != 201):
        message = replyErrorEmail(ticket.title, [ticket.email],
                                  formdata['ticketid'], json_data['message'])
        if current_app.config['SEND_MAIL_ON_MESSAGE']:
            app = current_app._get_current_object()
            thr = Thread(target=sendAsyncEmail, args=[message, app])
            thr.start()
    return msg


def somethingWentWrongMessage(subject, email, part, message):
    '''
    Send an email to the student,
    informing them that something went wrong with creating their ticket.
    '''
    message = somethingWentWrong(subject, [email], part, message)
    app = current_app._get_current_object()
    thr = Thread(target=sendAsyncEmail, args=[message, app])
    thr.start()


@apiBluePrint.route('/email/<course_id>/settings', methods=['GET'])
def retrieveEmailSettings(course_id):
    '''
    Retrieve the email settings of a course.
    '''
    # Find the course in the database.
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response('This course does no longer exists',
                                         200)

    # Check if a thread exists.
    thread = MailThread.existThreadCourseID(course_id)
    running = False
    if (thread is not None):
        running = True

    object = {'email': course.course_email, 'password': course.mail_password,
              'port': course.mail_port, 'pop': course.mail_server_url,
              'running': running}

    return Iresponse.create_response(object, 201)


@apiBluePrint.route('/email/<course_id>/online', methods=['GET'])
def isEmailFetching(course_id):
    '''
    Returns if an email fetcher is already running.
    '''
    # Find the thread and check if it's running.
    thread = MailThread.existThreadCourseID(course_id)
    running = False
    if (thread is not None):
        running = True

    object = {'running': running}

    return Iresponse.create_response(object, 201)


@apiBluePrint.route('/email/labels/<course_id>', methods=['GET'])
def email_retrieve_labels(course_id):
    """
    Returns all labels of given course.
    TODO: Controle if user has permissions.
    """
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("", 404)
    return Iresponse.create_response(
        database.serialize_list(course.labels), 200)


@apiBluePrint.route('/email/stop', methods=['POST'])
def stopEmailFetching():
    '''
    Stop the fetching of emails.
    '''
    # Find the thread and check if it's running.
    course_id = escape(request.json['course_id'])
    thread = MailThread.existThreadCourseID(course_id)

    if (thread is None):
        return Iresponse.create_response('No email thread running', 200)

    thread.stop()
    return Iresponse.create_response('Succes', 201)
