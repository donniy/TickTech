from flaskr.models.ticket import *
from . import apiBluePrint
from mail.fetch import MailThread


@apiBluePrint.route('/fetch', , methods=['POST'])
def submit():
    sleeptime = 10
    server = escape(request.json["pop"])
    port = escape(request.json["port"])
    email = escape(request.json["email"])
    password = escape(request.json["password"])
    create_new_email_thread(sleeptime, server, port, email, password)

def create_new_email_thread(sleeptime, server, port, email, password):
    """
    Create a new email thread
    """
    print("create new thread")
    new_thread = MailThread(sleeptime, server, port, email, password)

    new_thread.run()
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
