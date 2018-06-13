from . import apiBluePrint
from mail.thread import MailThread
from flaskr.models.Course import Course
from flaskr import database, Iresponse
from flask import escape, request, jsonify
import poplib


@apiBluePrint.route('/email', methods=['POST'])
def create_new_email_thread_post():
    '''
    Recieve email settings from website. Update it in database and send to
    mail server.
    '''
    # Time between fetching emails
    sleeptime = 60
    # Try to make a connection
    try:
        server = escape(request.json["pop"])
        port = escape(request.json["port"])
        email = escape(request.json["email"])
        password = escape(request.json["password"])
        course_id = escape(request.json["course_id"])
        test_connection = poplib.POP3_SSL(server, port)
        test_connection.user(email)
        test_connection.pass_(password)
        test_connection.quit()
        print("Succesfull test connection")
    except (poplib.error_proto) as msg:
        message = msg.args[0].decode('ascii')
        return Iresponse.create_response(message, 200)
    except:
        return Iresponse.create_response("Invalid settings", 200)

    course = Course.query.get(course_id)
    course.course_email = email
    course.mail_password = password
    course.mail_port = port
    course.mail_server_url = server
    if not database.addItemSafelyToDB(course):
        return Iresponse.create_response("Failed to attach to database", 412)

    create_new_email_thread(sleeptime, server, port, email,
                            password, course_id)
    return Iresponse.create_response("Succes", 201)


@apiBluePrint.route('/email/<course_id>/settings', methods=['GET'])
def retrieve_current_mail_settings(course_id):
    """
    Geeft email instelling van course.
    """
    # TODO: Controlleer rechten
    course = Course.query.get(course_id)
    if course is None:
        return Iresponse.create_response("This course does no longer exists", 200)

    thread = MailThread.exist_thread_courseid(course_id)
    running = False
    if (thread is not None):
        running = True

    object = {'email': course.course_email, 'password': course.mail_password,
              'port': course.mail_port, 'pop': course.mail_server_url,
              'running': running}

    return Iresponse.create_response(object, 201)


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


def create_new_email_thread(sleeptime, server, port, email, password,
                            course_id):
    """
    Create a new email thread
    """
    thread = MailThread.exist_thread_courseid(course_id)
    if (thread is None):
        print("create new thread")
        new_thread = MailThread(sleeptime, server, port, email, password,
                                course_id)
        new_thread.setName(course_id)
        new_thread.start()
        print("done")
    else:
        print("Thread already exists, update")
        update_thread(thread, sleeptime, server, port, email, password)
    return


def stop_thread(thread):
    """
    Stop an existing email thread
    """
    thread.stop()
    return


def update_thread(thread, sleeptime, server, port, email, password):
    """
    Update an existing thread.
    """
    # One example
    print("Updating thread..")
    thread.update(sleep_time=sleeptime, server=server, port=port, email=email,
                  password=password)
    return
