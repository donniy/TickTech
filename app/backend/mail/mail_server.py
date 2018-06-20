from email.header import decode_header
from time import sleep
import email
import poplib
import requests
import html2text

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


def parse_email(bytes_email):
    '''
    Parses a raw email. Returns the subject, body and sender in string format.
    '''
    # Parse email.
    parsed_email = email.message_from_bytes(bytes_email)

    # Get subject.
    subject_parsed = decode_header(parsed_email['Subject'])
    if subject_parsed[0][1] is not None:
        subject = subject_parsed[0][0].decode(subject_parsed[0][1])
    else:
        subject = subject_parsed[0][0]

    # Get body.
    body = ''
    html = ''
    files = {}
    attachments = []
    print("parsing body")
    if parsed_email.is_multipart():
        for part in parsed_email.walk():
            ctype = part.get_content_type()
            if (ctype == 'text/plain'):
                body += str(part.get_payload())
            elif ctype in ['image/jpeg', 'image/png']:
                # What yo do with the attachment?!
                # open(part.get_filename(), 'wb')
                # .write(part.get_payload(decode=True))
                print("THIS IS TYPE: ", type(part.get_payload(decode=True)))
                print("Found image")
                files[part.get_filename()] = part.get_payload(decode=True)
            elif ctype == "text/html":
                html += str(part.get_payload())
            else:
                ctype_split = ctype.split('/')
                print("splitted", ctype_split)
                if (ctype_split[0] == 'text'):
                    print("Attachment text")
                    print("THIS IS TYPE: ", type(part.get_payload(decode=True)))
                    print("Found:",ctype_split[1])
                    files[part.get_filename()] = part.get_payload(decode=True)
    else:
        # Emails are always multipart?
        if (parsed_email.get_content_type() == 'text/plain'):
            body += str(parsed_email.get_payload())
        elif parsed_email.get_content_type() == "text/html":
            html += str(part.get_payload())
        else:
            print("Not multipart and  not plain")

    if body == '':
        body += html2text.html2text(html)

    # Get sender.
    sender_parsed = decode_header(parsed_email['From'])
    if sender_parsed[0][1] is not None:
        sender = sender_parsed[0][0].decode(sender_parsed[0][1])
    else:
        sender = sender_parsed[0][0]

    # Sender is of format "Firstname Lastname <email@email.com>".
    print(sender, '\n\n')
    try:
        name = sender.split("<")
        address = name[1].split(">")
    except IndexError:
        name = sender
        address = sender

    return subject, body, files, name[0], address[0]


def find_user_id(body, sender, sendermail):
    '''
    Parses a given body in string format. Returns the student id,
    name and label, if possible.
    '''

    print("Trying to link user to this email", sender, sendermail)
    info = {
        'email': sendermail
    }
    result = requests.post(
        'http://localhost:5000/api/email/user/match',
        json=info)

    #sprint(result.text)
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


def retrieve_labels(courseid):
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
        print("Failed", result.text)

    return labels


def check_mail(host, port, user, password, courseid):
    '''
    Start a mail server and sync all emails once.
    '''
    # connect
    server = connect(host, port, user, password)
    # Cannot connect. Try again later
    if server is None:
        return 1

    mailcount = server.stat()[0]
    if (mailcount == 0):
        print("No emails found.")
        server.quit()
        return 0
    else:
        print(mailcount, "emails found. parsing...")

    # Get all labels available for this course
    labels = retrieve_labels(courseid)
    for i in range(mailcount):

        # parse email
        bytes_email = b"\n".join(server.retr(i + 1)[1])
        subject, body, files, sender, address = parse_email(bytes_email)

        #print("FILES:", files)

        # Check for succes
        if (subject is None or body is None or sender is None):
            print("Error parsing email.")
            print("subject", subject)
            print('body', body)
            print('sender', sender)
        else:
            # validate user
            studentid = find_user_id(body, sender, address)
            if studentid is None:
                # TODO: What to do?
                studentid = 123123123

            # Check if email with subject exists

            # Try To attach label
            if (labels != []):
                labelid = labels[0]['label_id']
            else:
                labelid = None
            #print("CHECKLABEL:",labelid, labels)

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
                json=newticket, files=files)

            print("RESULT:", result.status_code)
            if (result.status_code != 201):
                print("Something went wrong creating a"
                      "new ticket from an email.")
                print(result.text)
                print("******")
                print("Sender: " + str(sender) + "\nStudentid: " +
                      str(studentid) + "\nEmail: " + str(address) +
                      "\nSubject: " + str(subject))
                print("Course ID: ", courseid)
                print("Label ID: ", labelid, "\n\n")
                print("Body: " + body)
            else:
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
