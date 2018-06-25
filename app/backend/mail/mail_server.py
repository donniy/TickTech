from email.header import decode_header
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

            # If not html or plain text, check if it's some kind of file.
            # ATTACHMENT DONT WORK YET
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
            print("Not multipart and not plain. ")

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


def findUser(body, sender, sendermail):
    '''
    Parses a given emailbody in string format. Returns the student id,
    name and label, if possible.
    '''

    print("Trying to link user to this email", sender, sendermail)
    
    info = {
        'email': sendermail
    }

    result = requests.post(
        'http://localhost:5000/api/email/user/match',
        json=info)

    # sprint(result.text)
    # If request was succesful, check 
    if(result.status_code == 200):
        json = result.json()
        if (json['json_data']['succes']):
            id = json['json_data']['studentid']
            if id is not None:
                return id

    return None

    # body = body.split()
    # for words in body:
    #     if words.isdigit() and len(words) > 6 and len(words) < 9:
    # > old ids 6 digits, new ones 8.
    #         studentid = words
    #
    # TODO: find the keywords of labels in the text
    # if words in labels
    # labelid = words
    # print('Found matching label ID: ' + labelid)
    # return studentid, 1


def retrieveLabels(courseid):
    '''
    Retrieve all available labels of a course from the server.
    '''
    labels = None
    result = requests.get('http://localhost:5000/api/labels/' + courseid)
    if (result.status_code == 200):
        data = result.json()
        labels = data['json_data']
        if (labels == []):
            print("No labels available")
        else:
            # This is how it works
            print(labels[0]['label_id'], labels[0]['label_name'])
    else:
        print("Failed retrieving labels", result.text)

    return labels


def checkMail(host, port, user, password, courseid, debug=0):
    '''
    Start a mail server and sync all emails once.
    Set debug to anything but 0 to enable debugging. This will make sure
    emails will keep coming in.
    '''
    # Connect to the server.
    server = connect(host, port, user, password)
    
    # Cannot connect. Try again later.
    if server is None:
        return 1

    mailcount = server.stat()[0]
    if (mailcount == 0):
        print("No emails found. Quitting!")
        server.quit()
        return 0
    else:
        print(mailcount, "emails found. parsing...")

    # Get all labels available for this course
    labels = retrieveLabels(courseid)
    for i in range(mailcount):

        # parse email
        emailBytes = b"\n".join(server.retr(i + 1)[1])
        subject, body, files, sender, address = parseEmail(emailBytes)

        # print("FILES:", files)

        # Check for succes
        if (subject is None or body is None or sender is None):
            print("Error parsing email.")
            print("subject", subject)
            print('body', body)
            print('sender', sender)
        else:
            # validate user
            studentid = findUser(body, sender, address)
            if studentid is None:
                # TODO: What to do?
                studentid = 123123123

            # Check if email with subject exists

            # Try To attach label
            if (labels != []):
                labelid = labels[0]['label_id']
            else:
                labelid = ''
            # print("CHECKLABEL:",labelid, labels)

            newticket = {
                'name': sender,
                'studentid': studentid,
                'email': address,
                'subject': subject,
                'message': body,
                'courseid': courseid,
                'labelid': labelid
            }
            
            print("labelid", labelid)
            print("body=upload", body)

            attachments = {}
            for name, bytes in files:
                attachments[name] = base64.b64encode(bytes)

            newticket['files'] = attachments

            # Add the new variables to a new ticket.
            # print("HIERRR")
            # print(newticket)

            # result = requests.post(
            #     'http://localhost:5000/api/email/ticket/submit',
            #     json=newticket)

            # print("CREATED TICKET")

            # print("RESULT:", result.status_code)
            # if (result.status_code != 201):
            #     print("Something went wrong creating a"
            #           "new ticket from an email.")
            #     print("******")
            #     print("Sender: " + str(sender) + "\nStudentid: " +
            #           str(studentid) + "\nEmail: " + str(address) +
            #           "\nSubject: " + str(subject))
            #     print("Course ID: ", courseid)
            #     print("Label ID: ", labelid, "\n\n")
            #     print("Body: " + body)

    # Somehow makes you up-to-date with server
    # disable this when debugging
    if (debug == 0):
        server.quit()
    return 0


if __name__ == '__main__':
    # Retrieve courses, get current course id.
    result = requests.get('http://localhost:5000/api/courses')
    if (result.status_code == 200):
        courses = result.json()
        courseid = courses["json_data"][0]["id"]
    else:
        print(result.status_code)
        # print("Failed", result.text)

    # Check mail for current course.
    checkMail("pop.gmail.com", "995",
               "uvapsetest@gmail.com", "stephanandrea", courseid)
    print("Finished")
