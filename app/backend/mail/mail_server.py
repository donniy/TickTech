from email.header import decode_header
from time import sleep
import poplib
import email
import requests

def connect(host, port, user, password):
    '''
    Connects to and authenticates with a POP3 mail server. Returns None on failure

    return: server_connection
    '''
    M = None
    try:
        #print("Connecting to ", user)
        M = poplib.POP3_SSL(host, port)
        M.user(user)
        M.pass_(password)
        #print("Succesfully connected\n")
    except (poplib.error_proto) as msg:
        raise 'Connection error: ' + msg

    return M


def parse_email(mail_box, i):
    '''
    Parse raw email.
    Returns subject and body and sender in string format
    '''
    # Parse email
    raw_email  = b"\n".join(mail_box.retr(i+1)[1])
    parsed_email = email.message_from_bytes(raw_email)

    ##print(parsed_email.keys()) #temp info

    # Get sender
    sender_parsed = decode_header(parsed_email['From'])
    if (sender_parsed[0][1] != None):
        senderline = sender_parsed[0][0].decode(sender_parsed[0][1])
    else:
        senderline = sender_parsed[0][0]
    
    sender = senderline.split("<")
    address = sender[1].split(">")

    # Get subject
    subject_parsed = decode_header(parsed_email['Subject'])
    if (subject_parsed[0][1] != None):
        subject = subject_parsed[0][0].decode(subject_parsed[0][1])
    else:
        subject = subject_parsed[0][0]
    #print(subject)

    # Get body
    body = None
    if parsed_email.is_multipart():
        #print("Multipart email")
        for payload in parsed_email.get_payload():
            if (payload.get_content_type() == "text/plain"):
                body = payload.get_payload()
    else:
        print("TODO: Not multipart email") #TODO: replies on emails
        #print(parsed_email.get_payload())

    return subject, body, sender[0], address[0]

def parse_body(body, courseid):
    '''
    Parse raw body.
    Returns the student id, name and label, if possible.
    '''
    new_body = body.split()

    for words in new_body:
        if words.isdigit() and len(words) > 6 and len(words) < 10: # > old ids 6 digits, new ones 8.
            studentid = words
            print('Student ID: ' + studentid)

        
        # TODO: find all labels of course id in database
        # labels = Label.query.get(courseid)
        # for label in labels:
            #  

        # 
    return studentid, 1

def check_mail(host, port, user, password):
    '''
    Start mail server
    '''
    server = connect(host, port, user, password)
    number_of_mails = server.stat()[0]
    #print("Mail:",number_of_mails ,"emails")
    #print("Size:",server.stat()[1],"bytes")

    # No new emails
    if (number_of_mails == 0):
        print("No emails")
        # server.quit()
        return

    for i in range(number_of_mails):
        # Get subject, body, sender from raw email
        subject, body, sender, address = parse_email(server, i)

        # TODO: Find course id for labels?
        studentid, labelid = parse_body(body, 5)
        if (subject == None or body == None or sender == None):
            print("Error parsing emails")
        else:
            print("Finished parsing mail. \nSubject: " + subject + "\nBody: '" + body + "'\nSender: "+ sender)
            payload =  {
                'name': sender, # parsing name from email - might not match database with personal emails?
                'studentid': studentid, # parse student id, or find in database based on email address ?
                'email': address,
                'message': body,
                'courseid': 1, # get course id from mail server (database)
                'labelid': "test", # compare body to label possibilities
                'subject': subject}

            #make a POST request
            res = requests.post('http://localhost:5000/api/ticket/submit', json=payload)
            print(res)

    # Somehow makes you up-to-date with server
    # disable this when debugging
    # server.quit()
    return
