from . import apiBluePrint
from mail.fetch import MailThread
from flaskr.models.Course import Course
from flaskr import database, Iresponse
from flask import escape, request, jsonify


@apiBluePrint.route('/email', methods=['POST'])
def submit():
    sleeptime = 10
    server = escape(request.json["pop"])
    port = escape(request.json["port"])
    email = escape(request.json["email"])
    password = escape(request.json["password"])
    create_new_email_thread(sleeptime, server, port, email, password)
    #TODO: Url van ticket in repsonse
    return Iresponse.create_response("", 201)

@apiBluePrint.route('/email/<course_id>/settings', methods=['GET'])
def retrieve_current_mail_settings(course_id):
    """
    Geeft email instelling van course.
    """
    print("GOT HERE\n\n\n\n")
    # TODO: Controlleer rechten
    ticketObj = Course.query.get(course_id)
    if ticketObj is None:
        print("No email")
        return Iresponse.create_response("", 404)

    print("Found email")
    return Iresponse.create_response(ticketObj.serialize, 200)


def create_new_email_thread(sleeptime, server, port, email, password):
    """
    Create a new email thread
    """
    print("create new thread")
    new_thread = MailThread(sleeptime, server, port, email, password)
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
