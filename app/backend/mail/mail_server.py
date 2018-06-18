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
        print(msg)
        return None
    except socket.gaierror as msg:
        print(msg)
        return None
    except OSError as msg:
        print(msg)
        return None

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
    if subject_parsed[0][1] is not None:
        subject = subject_parsed[0][0].decode(subject_parsed[0][1])
    else:
        subject = subject_parsed[0][0]

    # Get body.
    body = ''
    attachments = []
    if parsed_email.is_multipart():
        for part in parsed_email.walk():
            ctype = part.get_content_type()
            if (ctype == 'text/plain'):
                body += str(part.get_payload())
            if ctype in ['image/jpeg', 'image/png']:
                # What yo do with the attachment?!
                # open(part.get_filename(), 'wb')
                # .write(part.get_payload(decode=True))
                print("Found image")
    else:
        print("TODO: Not multipart email.")  # TODO: replies on emails
        # print(parsed_email.get_payload())

    # Get sender.
    sender_parsed = decode_header(parsed_email['From'])
    if sender_parsed[0][1] is not None:
        sender = sender_parsed[0][0].decode(sender_parsed[0][1])
    else:
        sender = sender_parsed[0][0]

    # Sender is of format "Firstname Lastname <email@email.com>".
    name = sender.split("<")
    address = name[1].split(">")

    return subject, body, name[0], address[0]


def parse_body(string, courseid):
    '''
    Parses a given body in string format. Returns the student id,
    name and label, if possible.
    '''
    # TODO: get the right labels from database with the courseid
    # Perhaps query keywords of labels of all courses ?
    # labels = Label.query.get(courseid)
    # keywords = ??

    body = string.split()
    studentid = 123123123

    for words in body:
        if words.isdigit() and len(words) > 6 and len(words) < 9:
            # > old ids 6 digits, new ones 8.
            studentid = words

        # TODO: find the keywords of labels in the text
        # if words in labels
        # labelid = words
        # print('Found matching label ID: ' + labelid)
    return studentid, 1


def check_mail(host, port, user, password, courseid):
    '''
    Start a mail server.
    '''
    server = connect(host, port, user, password)

    if server is None:
        # Cannot connect. Try again later
        return 1

    mailcount = server.stat()[0]
    if (mailcount == 0):
        print("No emails found.")
        server.quit()
        return 0

    # Get all labels available for this course
    labels = None
    result = requests.get('http://localhost:5000/api/labels/'+courseid)
    if (result.status_code == 200):
        data = result.json()
        labels = data['json_data']
        if (labels == []):
            print("No labels available")
        else:
            # This is how it works
            print(labels[0]['label_id'], labels[0]['label_name'])
    else:
        print("Failed", result.text)

    for i in range(mailcount):
        subject, body, sender, address = parse_email(server, i)

        if (subject is None or body is None or sender is None):
            print("Error parsing email.")
        else:
            studentid, labelid = parse_body(body, courseid)

            print("Sender: " + str(sender) + "\nStudentid: " + str(studentid) +
                  "\nEmail: " + str(address) + "\nSubject: " + str(subject))
            print("Course ID: ", courseid)
            print("Label ID: ", labelid, "\n\n")
            print("Body: " + body)

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
            result = requests.post(
                'http://localhost:5000/api/email/ticket/submit',
                json=newticket)

            if (result.status_code != 201):
                print("Something went wrong creating a"
                      "new ticket from an email.")
                print(result.text)

    # Somehow makes you up-to-date with server
    # disable this when debugging
    # server.quit()
    return 0


if __name__ == '__main__':
    print("Run this")
    result = requests.get('http://localhost:5000/api/courses')
    if (result.status_code == 200):
        courses = result.json()
        courseid = courses["json_data"][0]["id"]
    else:
        print("Failed", result.text)

    check_mail("pop.gmail.com", "995",
               "uvapsetest@gmail.com", "stephanandrea", courseid)
    print("Finished")
