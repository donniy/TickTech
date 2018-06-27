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
    thr = Thread(target=send_async_email,args=[message, app])
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
    # print(files.keys())

    if(len(files.keys()) > 5):
        return Iresponse.create_response("Too many files", 400)

    file_names = list()
    for filename in files.keys():
        # print("FILE", filename)
        file = base64.b64decode(files[filename])

        if not rp_file.save_file_from_mail(file, filename, file_names):
            # print("invalid file")
            return Iresponse.create_response("File too large", 400)
    formdata['files'] = file_names

    if not json_validation.validate_json(formdata, ['message',
                                                    'subject',
                                                    'courseid',
                                                    'labelid']):
        return Iresponse.create_response("Malformed request", 400)

    if not course_validation.check_course_validity(formdata['courseid'],
                                                   formdata['labelid']):
        for file in file_names:
            rp_file.remove_file(file)
        return Iresponse.create_response("Invalid Course/Label", 400)

    if not json_validation.validate_ticket_data(formdata):
        for file in file_names:
            rp_file.remove_file(file)
        return Iresponse.create_response("Invalid ticket data", 400)

    response = rp_ticket.create_request(formdata)

    if (response.status_code == 201):
        ticketid = response.get_json()['json_data']['ticketid']
        message = createdTicketEmail(formdata['subject'],
                                     [formdata['email']],
                                     ticketid,
                                     formdata['message'])
        app = current_app._get_current_object()
        thr = Thread(target=send_async_email,args=[message, app])
        thr.start()
        
    return response


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
    return if email is already running
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

#
# def create_new_email_thread(sleeptime, server, port, email, password,
#                             course_id):
#     """
#     Create a new email thread
#     """
#     thread = MailThread.exist_thread_courseid(course_id)
#     if (thread is None):
#         print("create new thread")
#         new_thread = MailThread(sleeptime, server, port, email, password,
#                                 course_id)
#         new_thread.setName(course_id)
#         new_thread.start()
#         print("done")
#     else:
#         print("Thread already exists, update")
#         update_thread(thread, sleeptime, server, port, email, password)
#     return
#
#
# def stop_thread(thread):
#     """
#     Stop an existing email thread
#     """
#     thread.stop()
#     return
#
#
# def update_thread(thread, sleeptime, server, port, email, password):
#     """
#     Update an existing thread.
#     """
# One example
#     print("Updating thread..")
#     thread.update(sleep_time=sleeptime, server=server, port=port,
#                   email=email, password=password)
#     return

# @apiBluePrint.route('/email', methods=['POST'])
# def notify_succes():
#     print("Got notify\n\n")
#     emit('setup-email', {'result': 'succes'})
#     print("emmited")
#     return Iresponse.create_response("succes", 200)
# def create_new_email_thread_post():
#     '''
#     Recieve email settings from website. Update it in database and send to
#     mail server.
#     '''
# Time between fetching emails
#     sleeptime = 60
#     server = escape(request.json["pop"])
#     port = escape(request.json["port"])
#     email = escape(request.json["email"])
#     password = escape(request.json["password"])
#     course_id = escape(request.json["course_id"])
#
#     try:
#         test_connection = poplib.POP3_SSL(server, port)
#         print(test_connection)
#         test_connection.user(email)
#         test_connection.pass_(password)
#         test_connection.quit()
#         print("Succesfull test connection")
#     except (poplib.error_proto) as msg:
#         print("failed")
#         message = msg.args[0].decode('ascii')
#         return Iresponse.create_response(message, 200)
#     except OSError as msg:
#         message = str(msg)
#         return Iresponse.create_response(message, 200)
#     except:
#         return Iresponse.create_response("Invalid settings", 200)
#
#     create_new_email_thread(sleeptime, server, port, email,
#                             password, course_id)
#
#     course = Course.query.get(course_id)
#     course.course_email = email
#     course.mail_password = password
#     course.mail_port = port
#     course.mail_server_url = server
#     if not database.addItemSafelyToDB(course):
#        return Iresponse.create_response("Failed to attach to database", 412)
#
#     return Iresponse.create_response("wait for further instruction", 201)
