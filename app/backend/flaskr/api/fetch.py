from . import apiBluePrint
from mail.fetch import MailThread
from flask import escape, request, jsonify

@apiBluePrint.route('/fetch/submit', methods=['POST'])
def submit():
    print("Gott here")
    sleeptime = 10
    server = escape(request.json["pop"])
    port = escape(request.json["port"])
    email = escape(request.json["email"])
    password = escape(request.json["password"])
    create_new_email_thread(sleeptime, server, port, email, password)
    return jsonify({'status': "success", 'message': "message.serialize"})

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
