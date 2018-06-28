from . import apiBluePrint
from flaskr.models.Course import Course
from flaskr.models.user import User
from flaskr import Iresponse
from flaskr.request_processing import ticket as rp_ticket
from flaskr.request_processing import file as rp_file
from flaskr.utils import course_validation, json_validation
from flask import escape, request
from flaskr.utils.json_validation import validate_json
from mail.thread import MailThread
from mail.Message import ticketErrorEmail, createdTicketEmail
from mail.Message import somethingWentWrong, replyErrorMail
from flask_mail import Mail
from threading import Thread
from flask import current_app
import base64


def send_async_email(message, app):
    with app.app_context():
        Mail().send(message)


@apiBluePrint.route('/email/user/match/email', methods=["POST"])
def mail_match_on_mail():
    """
    Try to match incomming email on email-address.
    """
    # Check data
    json_data = request.get_json()
    if not validate_json(json_data, ["email"]):
        return Iresponse.empty_json_request()

    # Match on first succes
    email = json_data["email"]
    user = User.query.filter_by(email=email).first()

    if user is not None:
        id = user.id
        success = True
    else:
        id = None
        success = False
    response = {
        "success": success,
        "studentid": id
    }
    return Iresponse.create_response(response, 200)


@apiBluePrint.route('/email/user/match/studentid', methods=["POST"])
def mail_match_on_studentid():
    '''
    Try to match incomming email on studentid.
    '''
    # Check data
    json_data = request.get_json()
    if not validate_json(json_data, ["studentid"]):
        return Iresponse.empty_json_request()

    # Match on first succes
    studentid = json_data["studentid"]
    user = User.query.filter_by(id=studentid).first()

    if user is not None:
        id = user.id
        success = True
    else:
        id = None
        success = False
    response = {
        "success": success,
        "studentid": id
    }
    return Iresponse.create_response(response, 200)


@apiBluePrint.route('/email/user/match/failed', methods=["POST"])
def mail_notify_failed_match():
    '''
    Notify user that mail failed to match.
    '''
    # Check data
    json_data = request.get_json()
    if not validate_json(json_data, ["body", "subject", "address"]):
        return Iresponse.empty_json_request()

    # Match on first succes
    subject = json_data["subject"]
    address = json_data["address"]
    body = json_data["body"]

    message = ticketErrorEmail(subject, [address], body)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[message, app])
    thr.start()

    return Iresponse.create_response('Success', 200)


@apiBluePrint.route('/email/ticket/submit', methods=['POST'])
def create_email_ticket():
    """
    Check ticket submission and add to database.
    """
    # Mandatory check to comply with incompatible testing.

    formdata = request.get_json()
    files = formdata['files']

    if(len(files.keys()) > 5):
        something_went_wrong_message(formdata['subject'],
                                     formdata['email'],
                                     'To many files'
                                     formdata['message'])
        return Iresponse.create_response("Too many files", 400)

    file_names = list()
    for filename in files.keys():
        file = base64.b64decode(files[filename])

        if not rp_file.save_file_from_mail(file, filename, file_names):
            something_went_wrong_message(formdata['subject'],
                                         formdata['email'],
                                         'File to large'
                                         formdata['message'])
            return Iresponse.create_response("File too large", 400)
    formdata['files'] = file_names

    if not json_validation.validate_json(formdata, ['message',
                                                    'subject',
                                                    'courseid',
                                                    'labelid']):
        something_went_wrong_message(formdata['subject'],
                                     formdata['email'],
                                     'validate json data'
                                     formdata['message'])
        return Iresponse.create_response("Malformed request", 400)

    if not course_validation.check_course_validity(formdata['courseid'],
                                                   formdata['labelid']):
        for file in file_names:
            rp_file.remove_file(file)
        return Iresponse.create_response("Invalid Course/Label", 400)

    if not json_validation.validate_ticket_data(formdata):
        for file in file_names:
            rp_file.remove_file(file)
        something_went_wrong_message(formdata['subject'],
                                     formdata['email'],
                                     'validate ticket data'
                                     formdata['message'])
        return Iresponse.create_response("Invalid ticket data", 400)

    response = rp_ticket.create_request(formdata)

    if (response.status_code == 201):
        ticketid = response.get_json()['json_data']['ticketid']
        message = createdTicketEmail(formdata['subject'],
                                     [formdata['email']],
                                     ticketid,
                                     formdata['message'])
        app = current_app._get_current_object()
        thr = Thread(target=send_async_email, args=[message, app])
        thr.start()

    return response

@apiBluePrint.route('/email/ticket/email/newmessage', methods=['POST'])
def create_email_message():
    """
    Add message in existing ticket.
    """
    formdata = request.get_json()
    if not json_validation.validate_json(formdata, ['ticketid']):
        something_went_wrong_message(formdata['subject'],
                                     formdata['email'],
                                     'validate json data'
                                     formdata['message'])
        return Iresponse.create_response("Malformed request", 400)

    ticket = Ticket.query.get(formdata['ticketid'])
    if ticket is None:
        something_went_wrong_message(formdata['subject'],
                                     formdata['email'],
                                     'Could not find ticket with that id'
                                     formdata['message'])
        return Iresponse.create_response("Could not find ticket", 400)

    formdata["studentid"] = ticket.user_id

    msg = rp_message.create_request(formdata, formdata['ticketid'])

    if (msg.status_code != 201)
        message = replyErrorMail(ticket.title,
                                     [ticket.email], formdata['ticketid'],
                                     json_data['message'])
        if current_app.config['SEND_MAIL_ON_MESSAGE']:
            app = current_app._get_current_object()
            thr = Thread(target=send_async_email, args=[message, app])
            thr.start()
    return msg



def something_went_wrong_message(subject, email, part, message):
    '''
    Send mail to user that something went wrong with creating his ticket.
    '''
    message = somethingWentWrong(subject,
                                 [email],
                                 part,
                                 message)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[message, app])
    thr.start()

@apiBluePrint.route('/email/<course_id>/settings', methods=['GET'])
def retrieve_current_mail_settings(course_id):
    """
    Give mail settings of course.
    """
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("This course does no longer exists",
                                         200)

    thread = MailThread.exist_thread_courseid(course_id)
    running = False
    if (thread is not None):
        running = True

    object = {'email': course.course_email, 'password': course.mail_password,
              'port': course.mail_port, 'pop': course.mail_server_url,
              'running': running}

    return Iresponse.create_response(object, 201)


@apiBluePrint.route('/email/<course_id>/online', methods=['GET'])
def is_email_running(course_id):
    """
    return if email is already running.
    """
    thread = MailThread.exist_thread_courseid(course_id)
    running = False
    if (thread is not None):
        running = True
    object = {'running': running}
    return Iresponse.create_response(object, 201)

#  This can be added if needed, currently not used
# @apiBluePrint.route('/email/force/<course_id>/fetch', methods=['POST'])
# def force_fetch_email(course_id):
#     """
#     Force a one time email fetch
#     """
#     thread = MailThread.exist_thread_courseid(course_id)
#     if (thread is not None):
#         thread.force_fetch()
#         message = "succes"
#     else:
#         message = "failed, thread not found"
#     result = {'status': message}
#     return Iresponse.create_response(result, 200)


@apiBluePrint.route('/email/stop', methods=['POST'])
def stop_email_fetching():
    """
    Stop email fetching.
    """
    course_id = escape(request.json["course_id"])
    thread = MailThread.exist_thread_courseid(course_id)
    if (thread is None):
        return Iresponse.create_response("No email thread running", 200)
    thread.stop()
    return Iresponse.create_response("Succes", 201)
