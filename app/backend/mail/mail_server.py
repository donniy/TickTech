from email.header import decode_header
from flask_mail import Mail
from mail.Message import ticketErrorEmail
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

    # Parse the body of the email.
    body, html, attachments, files = parseBody(parsedEmail)

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


def parseBody(parsedEmail):
    body = ''
    html = ''
    attachments = []
    files = {}

    # Add all text and html to the final body.
    if parsedEmail.is_multipart():
        for part in parsedEmail.walk():
            ctype = part.get_content_type()
            if (ctype == 'text/plain'):
                body += str(part.get_payload())
            elif ctype == "text/html":
                html += str(part.get_payload())
            # If not html or plain text, check if it's some kind of file.
            else:
                data = part.get_payload(decode=True)
                ctype_split = ctype.split('/')
                try:
                    if (ctype_split[0] == 'text' or ctype_split[0] == 'image'):
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

    return body, html, attachments, files


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

    # Parse for studentd ids: Old student ids are 6 digits long, new ones are 8.
    body = body.split()
    for words in body:
        if words.isdigit() and len(words) > 6 and len(words) < 9:
            return int(words)

        # TODO: DIT WERKT NOG NIET?
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


# TODO: Labels wordt weer many to many in de backend via Ravi, dus dit moet weer aangepast worden straks.
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

def createReply(subject, body, files, sender, address, courseid):
    '''
    Create a reply to a ticket from the acquired information from an email.
    '''
    # TODO: Finish this functione.
    # # Find original ticket with subject / meta data? 
    
    # # Create a new reply.
    # newmessage = {}

    # # Add the reply to the database.
    # result = requests.post(SOMETHING, json=newmessage)

    # if (result.status_code != 201):
    # replyErrorMail()


def createTicket(subject, body, files, sender, address, courseid):
    '''
    Create a ticket from the acquired information from an email.
    Note: New tickets will only be displayed after refreshing the page.
    '''
    # Find student in database or by email parsing.
    studentid = findUser(body, sender, address)

    # If not found, send automatic reply that an error occurred.
    if studentid is None:
        print("SENDING ERROR")
        print(subject, address, body)
        message = ticketErrorEmail(subject, address, body)
        res = Mail().send(message)
        res = res  # for flake8
        return

    #   # TODO: Check if an email is a reply or a new email.
    #     # if "Re: " in subject:
    #     # Check the body for meta data? Ticket id in titel/body?
    #     # Check if user corresponds with original ticket
    #     createReply(subject, body, files, sender, address, courseid)
    #     else
    #         replyErrorMail(title, recipients, TODO TICKETID, body)
    #     return

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

    # Add attachments to tickets.
    attachments = {}
    for name, bytes in files:
        attachments[name] = base64.b64encode(bytes).decode("utf-8")
    newticket['files'] = attachments

    # Add the ticket to the database.
    result = requests.post(
        'http://localhost:5000/api/email/ticket/submit',
        json=newticket)

    if (result.status_code != 201):
        #ticketErrorEmail()
        print("Something went wrong creating a new ticket from an email.")
        print("******")
        print("Sender: " + str(sender) + "\nStudentid: " +
              str(studentid) + "\nEmail: " + str(address) +
              "\nSubject: " + str(subject))
        print("Course ID: ", courseid)
        print("Label ID: ", labelid)
        print("Body: " + body)

    # TODO: Send confirmation email.
    # createdTicketEmail(subject, address, TODO TICKETID, body)
    # res = Mail().send(message)
    # res = res  # for flake8
    # return

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
    if (debug == 0):
        server.quit()
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
