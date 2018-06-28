from email.header import decode_header
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import base64
import email
import html2text
import poplib
import re
import requests
import socket


poplib._MAXLINE = 2048


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
    Parses a raw email.
    Returns the subject, body and sender in string format.
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

    # Sender is either of the format "Firstname Lastname <email@email.com>"
    # or just plain email@email.com.
    try:
        name = sender.split("<")
        address = name[1].split(">")
        return subject, body, attachments, name[0], address[0]
    except IndexError:
        name = 'unknown'
        address = sender

    return subject, body, attachments, name, address


def parseBody(parsedEmail):
    '''
    Parses the body of an email.
    Returns the body and optional attachments on success.
    '''
    body = ''
    html = ''
    attachments = []
    files = {}

    # Add all text and html to the final body.
    if parsedEmail.is_multipart():
        for part in parsedEmail.walk():
            ctype = part.get_content_type()
            data = part.get_payload(decode=True)
            if (ctype == 'text/plain'):
                body += str(data.decode("utf-8"))
            elif ctype == "text/html":
                html += str(data.decode("utf-8"))
            # If not html or plain text, check if it's some kind of file.
            else:
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
            body += str(parsedEmail.get_payload(decode=True).decode("utf-8"))
        elif parsedEmail.get_content_type() == "text/html":
            html += str(parsedEmail.get_payload(decode=True).decode("utf-8"))
        else:
            print("Could not parse email. " +
                  "It was neither multipart nor plain.")

    return body, html, attachments, files


def requestStudentID(result):
    '''
    Helper function to send json request to retrieve information
    from the database. Returns studentid on success, None on failure.
    '''
    if (result.status_code == 200):
        json = result.json()
        if (json['json_data']['success']):
            studentid = json['json_data']['studentid']
            return studentid


def retrieveLabels(courseid):
    '''
    Helper function to retrieve all available labels of a
    course from the server.
    '''
    labels = []
    result = requests.get('http://localhost:5000/api/labels/' + courseid)

    if (result.status_code == 200):
        data = result.json()
        labels = data['json_data']

    return labels


def findLabel(body, labels):
    '''
    Parse the body for words that might be labels. Using the fuzzywuzzy module,
    a score will be calculated on the match of a substring.
    The UUID of the best match will be returned.
    '''
    # Put all labels in a list.
    labelcount = len(labels)
    result = []
    for i in range(0, labelcount):
        result.append(labels[i]['label_name'])

    bestScore = 0
    bestLabel = None

    # Find the best match between labels and the body of the e-mail.
    for i in range(0, labelcount):
        currentScore = fuzz.ratio(result[i], body)
        if (currentScore > 1):
            if (currentScore > bestScore):
                bestScore = currentScore
                bestLabel = labels[i]

    return bestLabel['label_id']


def findUser(body, sender, address):
    '''
    Parses a given email body in string format. Returns the student id,
    name and label, if possible, else None.
    '''
    # Check if the email is in the database.
    info = {'email': address}
    result = requests.post(
        'http://localhost:5000/api/email/user/match/email',
        json=info)

    # If request was succesful, try and connect mail to student id in database.
    if (requestStudentID(result) is not None):
        return requestStudentID(result)

    # Parse for studentd ids: Old ids are 6 digits long, new ones are 8.
    body = body.split()
    studentid = None
    for words in body:
        if (words.isdigit() and len(words) > 6 and len(words) < 9):
            studentid = int(words)

    # Check if the student id is in the database.
    info = {'studentid': studentid}
    result = requests.post(
        'http://localhost:5000/api/email/user/match/studentid',
        json=info)

    # Either return the student ID or None if not found.
    return requestStudentID(result)


def createReply(ticketid, subject, address, body):
    '''
    Create a reply to a ticket from the acquired information from an email.
    '''
    # Split body on old message
    newbody = re.split('(On )(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(,)', body, 1)[0]
    newbody = re.split('--------', newbody, 1)[0]

    # Create a new reply.
    newmessage = {
        'email': address,
        'ticketid': ticketid,
        'subject': subject,
        'message': newbody
    }

    # Add the reply to the database.
    result = requests.post(
        'http://localhost:5000/api/email/ticket/newmessage',
        json=newmessage)

    # Below is for debugging. An error mail will be send if
    # the reply is not posted.
    if (result.status_code != 201):
        print("Something went wrong creating a new reply from an email.")


def createTicket(subject, body, files, sender, address, courseid):
    '''
    Create a ticket from the acquired information from an email.
    Note: New tickets will only be displayed after refreshing the page.
    '''
    # Check if an email is a reply, if so,
    # a new message must be created instead of a new ticket.
    if "Ticket ID:" in subject:
        ticketid = subject.split("Ticket ID:")[1]
        ticketid = ticketid.replace("\n", "")
        ticketid = ticketid.replace(" ", "")
        createReply(ticketid, subject, address, body)
        return

    # Find student in database or by email parsing.
    sender = sender.replace(' ', '')
    studentid = findUser(body, sender, address)
    if studentid is None:
        info = {'subject': subject,
                'body': body,
                'address': address}

        # If result returned an error status code, an email is sent
        result = requests.post(
            'http://localhost:5000/api/email/user/match/failed',
            json=info)

        return

    # Get all labels available for this course, find the best matching one.
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

    # Below is for debugging. An errormail will be send if
    # the ticket is not posted.
    if (result.status_code != 201):
        print("Something went wrong creating a new ticket from an email.")
        print("******")
        print("Sender: " + str(sender) + "\nStudentid: " +
              str(studentid) + "\nEmail: " + str(address) +
              "\nSubject: " + str(subject))
        print("Course ID: ", courseid)
        print("Label ID: ", labelid)
        print("Body: " + body)


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
        print(mailcount, "new email(s) found. Parsing now!")

    # Parse all new emails.
    for i in range(mailcount):
        try:
            emailBytes = b"\n".join(server.retr(i + 1)[1])
        except poplib.error_proto:
            # We have no email information yet, so no warning possible.
            print("Found too many chars in a line, while parsing an email.")
            continue

        subject, body, files, sender, address = parseEmail(emailBytes)

        if (subject is None or body is None or sender is None):
            print("An error occurred while parsing email.")
            print("Found subject:", subject)
            print("Found body:", body)
            print("Found sender:", sender)
        else:
            createTicket(subject, body, files, sender, address, courseid)

    # Update with server, disable this when debugging.
    if (debug == 0):
        server.quit()
    return 0
