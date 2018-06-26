from email.header import decode_header
from flask_mail import Mail
import email
import poplib
import requests
import base64
import html2text
import socket


def connect(host, port, user, password):
    '''
    Connects to and authenticates with a POP3 mail server.
    Returns None on failure, server connection on success.
    '''
    server = None
    try:
        server = poplib.POP3_SSL(host, port)
        server.user(user)
        server.pass_(password)
    # Check if poplib raises any kind of error.
    except (poplib.error_proto) as msg:
        print(msg)
        return None
    # Check if the server address and name are valid.
    except socket.gaierror as msg:
        print(msg)
        return None
    # Check if any system-related errors are raised.
    except OSError as msg:
        print(msg)
        return None
    return server


def parseEmail(emailBytes):
    '''
    Parses a raw email. Returns the subject, body and sender in string format.
    '''
    # Parse the email.
    parsedEmail = email.message_from_bytes(emailBytes)

    # Get subject of email.
    subjectParsed = decode_header(parsedEmail['Subject'])
    if subjectParsed[0][1] is not None:
        subject = subjectParsed[0][0].decode(subjectParsed[0][1])
    else:
        subject = subjectParsed[0][0]

    # Get body of email.
    body = ''
    html = ''
    files = {}
    attachments = []

    # Add all text and html to the final body.
    if parsedEmail.is_multipart():
        for part in parsedEmail.walk():
            ctype = part.get_content_type()
            if (ctype == 'text/plain'):
                body += str(part.get_payload())
            elif ctype == "text/html":
                html += str(part.get_payload())

            # # TODO: fix ATTACHMENTS
            # # If not html or plain text, check if it's some kind of file.
            else:
                data = part.get_payload(decode=True)
                ctype_split = ctype.split('/')
                # print("splitted", ctype_split)
                try:
                    if (ctype_split[0] == 'text' or ctype_split[0] == 'image'):
                        # print("Attachment text")
                        # print("Found:", ctype_split[1])
                        attachments.append((part.get_filename(),
                                            data))
                        files[part.get_filename()] = data
                except IndexError:
                    print("Something wrong with MIMI type;",
                          ctype, ctype_split)
    else:
        # Emails are always multipart?
        if (parsedEmail.get_content_type() == 'text/plain'):
            body += str(parsedEmail.get_payload())
        elif parsedEmail.get_content_type() == "text/html":
            html += str(part.get_payload())
        else:
            print("Could not parse email. It was neither multipart nor plain.")

    # Transform html to text and add it to body.
    if body == '':
        body += html2text.html2text(html)

    # Get sender.
    sender_parsed = decode_header(parsedEmail['From'])
    if sender_parsed[0][1] is not None:
        sender = sender_parsed[0][0].decode(sender_parsed[0][1])
    else:
        sender = sender_parsed[0][0]

    # Sender is of format "Firstname Lastname <email@email.com>".
    try:
        name = sender.split("<")
        address = name[1].split(">")
    except IndexError:
        name = sender
        address = sender

    return subject, body, attachments, name[0], address[0]


def findUser(body, sender, address):
    '''
    Parses a given email body in string format. Returns the student id,
    name and label, if possible.
    '''
    # Create JSON to match email to user in the database.
    info = {'email': address}
    result = requests.post(
        'http://localhost:5000/api/email/user/match',
        json=info)

    # If request was succesful, try and connect mail to student id in database.
    if (result.status_code == 200):
        json = result.json()
        if (json['json_data']['succes']):  # ENGELS FOUT FIX HET
            studentid = json['json_data']['studentid']
            if studentid is not None:
                return studentid

    # Try and find a student id in the email body.
    body = body.split()
    for words in body:
        # > old ids 6 digits, new ones 8.
        if words.isdigit() and len(words) > 6 and len(words) < 9:
            return int(words)

        # DIT WERKT NOG NIET?
        #   File "/TickTech/app/backend/flaskr/utils/notifications.py", line 68, in notify
        #     'user_id':  user.id,
        # AttributeError: 'NoneType' object has no attribute 'id'

    # Couldn't find student id with email or in body.
    print("COULD NOT FIND STUDENT ID. :(")
    return None


def retrieveLabels(courseid):
    '''
    Retrieve all available labels of a course from the server.
    '''
    labels = []
    result = requests.get('http://localhost:5000/api/labels/' + courseid)

    if (result.status_code == 200):
        data = result.json()
        labels = data['json_data']

    return labels


# TODO: Labels wordt weer many to many in de backend, dus dit moet weer aangepast worden.
def findLabel(body, labels):
    '''
    Parse the body for words that might be labels (simplified, accepting first found).
    '''
    body = body.split()
    result = []

    labelcount = len(labels)
    for words in body:
        for i in range(0, labelcount):
            if words in labels[i]['label_name']:
                return labels[i]['label_id']

    return ''


def createTicket(subject, body, files, sender, address, courseid):
    '''
    Create a ticket from the acquired information from an email.
    '''
    # validate user
    studentid = findUser(body, sender, address)
    if studentid is None:
        # TODO: Send automatic reply that an error occurred, please contact mailing list.
        studentid = 123123123

    # Get all labels available for this course.
    labels = retrieveLabels(courseid)
    if (labels != []):
        labelid = findLabel(body, labels)
    else:
        labelid = ''

    newticket = {
        'name': sender,
        'studentid': studentid,
        'email': address,
        'subject': subject,
        'message': body,
        'courseid': courseid,
        'labelid': labelid
    }

    # Add attachments to tickets (works for img & text - STEPHAN??)
    attachments = {}
    for name, bytes in files:
        attachments[name] = base64.b64encode(bytes)
    newticket['files'] = attachments

    # TODO: fix printing in FLASKR terminal
    print("Hier onder print het nog rare dingen")

    # Add the ticket to the database.
    result = requests.post(
        'http://localhost:5000/api/email/ticket/submit',
        json=newticket)

    # TODO: remove this prints after debugging.
    print("Hier boven print het nog rare dingen")

    if (result.status_code != 201):
        print("Something went wrong creating a new ticket from an email.")
        print("******")
        print("Sender: " + str(sender) + "\nStudentid: " +
              str(studentid) + "\nEmail: " + str(address) +
              "\nSubject: " + str(subject))
        print("Course ID: ", courseid)
        print("Label ID: ", labelid)
        print("Body: " + body)
    else:
        print("CREATED A TICKET! :)")

    # sendReplyMail(address,
    #               "Dear " + sender + ", \n
    #               "We have received your email and ")
    # TODO: Send confirmation email.


#    @app.route("/")
# def sendReplyMail(receiver, message):
#     '''
#     Basic email reply for confirming a question has been received through email,
#     and created into a ticket, or to tell them there was an issue with the email.
#     '''

#     msg = Message("TEST" + message + "TEST",
#                   recipients=["uvapsetest@gmail.com"])
#     mail.send(msg)


def checkMail(host, port, user, password, courseid, debug=0):
    '''
    Start a mail server and sync all emails once.
    Set debug to anything but 0 to enable debugging. This will make sure
    emails will keep coming in.
    '''
    # Connect to the server.
    server = connect(host, port, user, password)
    if server is None:
        return 1

    mailcount = server.stat()[0]
    if (mailcount == 0):
        print("No new emails found. Quitting!")
        server.quit()
        return 0
    else:
        print(mailcount, "new email(s) found!")

    # Parse all new emails.
    for i in range(mailcount):
        emailBytes = b"\n".join(server.retr(i + 1)[1])
        subject, body, files, sender, address = parseEmail(emailBytes)

        # Check for success
        if (subject is None or body is None or sender is None):
            print("Error parsing email.")
            print("subject", subject)
            print("body", body)
            print("sender", sender)
        else:
            # Create a ticket with acquired information.
            createTicket(subject, body, files, sender, address, courseid)

    # Update with server, disable this when debugging.
    # if (debug == 0):
        # server.quit()
    return 0


# For debugging. Can be removed later (we use thread.py).
if __name__ == '__main__':
    # Retrieve courses, get current course id.
    result = requests.get('http://localhost:5000/api/courses')

    if (result.status_code == 200):
        courses = result.json()
        courseid = courses["json_data"][0]["id"]
    else:
        print("Could not retrieve courses, error code: ", result.status_code)

    # Check mail for current course.
    checkMail("pop.gmail.com", "995",
              "uvapsetest@gmail.com", "stephanandrea", courseid)
