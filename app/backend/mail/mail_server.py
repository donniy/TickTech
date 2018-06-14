from email.header import decode_header
from time import sleep
import email
import poplib
import requests

'''
Rabbitmqueue: Message mpass system between flask en mail server
'''


def connect(host, port, user, password):
    '''
    Connects to and authenticates with a POP3 mail server.
    Returns None on failure, server_connection on success.
    '''
    server = None

    try:
        server = poplib.POP3_SSL(host, port)
        server.user(user)
        server.pass_(password)
    except (poplib.error_proto) as msg:
        raise 'Connection error: ' + msg

    return server


def parse_email(inbox, i):
    '''
    Parses a raw email. Returns the subject, body and sender in string format.
    '''
    # Parse email.
    raw_email = b"\n".join(inbox.retr(i + 1)[1])
    parsed_email = email.message_from_bytes(raw_email)

    # Get subject.
    subject_parsed = decode_header(parsed_email['Subject'])
    if subject_parsed[0][1] is not none:
        subject = subject_parsed[0][0].decode(subject_parsed[0][1])
    else:
        subject = subject_parsed[0][0]

    # Get body.
    body = None
    if parsed_email.is_multipart():
        for payload in parsed_email.get_payload():
            if (payload.get_content_type() == "text/plain"):
                body = payload.get_payload()
    else:
        print("TODO: Not multipart email.")  # TODO: replies on emails
        # print(parsed_email.get_payload())

    # Get sender.
    sender_parsed = decode_header(parsed_email['From'])
    if sender_parsed[0][1] is not none:
        sender = sender_parsed[0][0].decode(sender_parsed[0][1])
    else:
        sender = sender_parsed[0][0]

    # Sender is of format "Firstname Lastname <email@email.com>".
    name = sender.split("<")
    address = name[1].split(">")

    return subject, body, name[0], address[0]


def parse_body(string, courseid):
    '''
    Parses a given body in string format. Returns the student id, name and
    label, if possible.
    '''
    # TODO: get the right labels from database with the courseid
    # Perhaps query keywords of labels of all courses ?
    # labels = Label.query.get(courseid)
    # keywords = ??

    body = string.split()
    studentid = -1

    for words in body:
        if words.isdigit() and len(words) > 6 and len(words) < 9:
            # > old ids 6 digits, new ones 8.
            studentid = words

        # TODO: find the keywords of labels in the text
        # if words in labels
        # labelid = words
        # print('Found matching label ID: ' + labelid)
    return studentid, 1


def check_mail(host, port, user, password, course_id):
    '''
    Start a mail server.
    '''
    server = connect(host, port, user, password)
    mailcount = server.stat()[0]

    if (mailcount == 0):
        print("No emails found.")
        server.quit()
        return

    # TEMP GET COURSE: STEPHHIE IS FIXING THIS :)
    courseid = None
    result = requests.get('http://localhost:5000/api/courses')
    if (result.status_code == 200):
        courses = result.json()
        courseid = courses["json_data"][0]["id"]
    else:
        print("Error retrieving course id from server.")
        return
    # TEMP GET COURSE: STEPHHIE IS FIXING THIS :)

    for i in range(mailcount):
        subject, body, sender, address = parse_email(server, i)

        if (subject is None or body is None or sender is None):
            print("Error parsing email.")
        else:
            studentid, labelid = parse_body(body, courseid)

            print("Sender: " + sender + "\nStudentid: " + studentid +
                  "\nEmail: " + address + "\nSubject: " + subject)
            print("Course ID: ", courseid)
            print("Label ID: ", labelid, "\n\n")
            # print("Body: " + body)

            # parsed, but should be compared with database
            # parsed, but should be compared with database
            newticket = {
                'name': sender,
                'studentid': studentid,
                'email': address,
                'subject': subject,
                'message': body,
                'courseid': courseid,
                'labelid': labelid
            }

            # Add the new variables to a new ticket.
            result = requests.post('http://localhost:5000/api/ticket/submit',
                                   json=newticket)

            if (result.status_code != 201):
                print("Something went wrong creating a new ticket from"
                      "an email.")

    # Somehow makes you up-to-date with server
    # disable this when debugging
    # server.quit()
    return
