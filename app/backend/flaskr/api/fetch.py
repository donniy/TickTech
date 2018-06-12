from . import apiBluePrint
from mail.fetch import MailThread
from flaskr.models.Course import Course
from flaskr import database, Iresponse
from flask import escape, request, jsonify


@apiBluePrint.route('/email', methods=['POST'])
def update_email_settings():
    '''
    Recieve email settings from website. Update it in database and send to mail
    server.
    '''
    sleeptime = 10
    server = escape(request.json["pop"])
    port = escape(request.json["port"])
    email = escape(request.json["email"])
    password = escape(request.json["password"])
    course_id = escape(request.json["course_id"])

    course = Course.query.get(course_id)
    course.course_email = email
    course.mail_password = password
    course.mail_port = port
    course.mail_server_url = server
    database.addItemSafelyToDB(course)

    create_new_email_thread(sleeptime, server, port, email, password, course_id)
    #TODO: Url van ticket in repsonse
    return Iresponse.create_response("", 201)

@apiBluePrint.route('/email/<course_id>/settings', methods=['GET'])
def retrieve_current_mail_settings(course_id):
    """
    Geeft email instelling van course.
    """
    # TODO: Controlleer rechten
    course = Course.query.get(course_id)
    if course is None:
        print("No course")
        return Iresponse.create_response("", 404)
    object = {'email':course.course_email, 'password':course.mail_password, 'port':course.mail_port, 'pop':course.mail_server_url}
    return Iresponse.create_response(object, 200)


def create_new_email_thread(sleeptime, server, port, email, password, course_id):
    """
    Create a new email thread
    """
    print("create new thread")
    new_thread = MailThread(sleeptime, server, port, email, password, course_id)
    new_thread.setName("No thread id yet")

    new_thread.start()
    return


def stop_thread(thread):
    """
    Stop an existing email thread
    """

    thread.stop()
    return

def update_thread(thread):
    """
    Update an existing thread.
    """
    # One example
    thread.update(sleep_time = 20)
    return
