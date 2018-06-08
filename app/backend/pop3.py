from email.header import decode_header
from time import sleep
import poplib
import email
import requests

def connect():
    '''
    Connects to and authenticates with a POP3 mail server. Returns None on failure

    return: server_connection
    '''
    M = None
    host = 'pop.gmail.com'
    port = '995'
    user = 'uvapsetest@gmail.com'
    password = 'stephanandrea'

    try:
        print("Connecting to ", user)
        M = poplib.POP3_SSL(host, port)
        M.user(user)
        M.pass_(password)
        print("Succesfully connected\n")
    except (poplib.error_proto) as msg:
        raise 'Connection error: ' + msg

    return M


def parse_email(mail_box):
    '''
    Parse raw email.

    Returns subject and body and sender in string format
    '''
    num_messages = len(mail_box.list()[1])
    if (num_messages == 0):
        return None, None, None

    for i in range(num_messages):
        print(i, "message:")

        # Parse email
        raw_email  = b"\n".join(mail_box.retr(i+1)[1])
        parsed_email = email.message_from_bytes(raw_email)

        #print(parsed_email.keys()) #temp info

        # Get sender
        sender_parsed = decode_header(parsed_email['From'])
        if (sender_parsed[0][1] != None):
            sender = sender_parsed[0][0].decode(sender_parsed[0][1])
        else:
            sender = sender_parsed[0][0]
        print(sender)

        # Get subject
        subject_parsed = decode_header(parsed_email['Subject'])
        if (subject_parsed[0][1] != None):
            subject = subject_parsed[0][0].decode(subject_parsed[0][1])
        else:
            subject = subject_parsed[0][0]
        print(subject)

        # Get body
        body = None
        if parsed_email.is_multipart():
            print("Multipart email")
            for payload in parsed_email.get_payload():
                if (payload.get_content_type() == "text/plain"):
                    body = payload.get_payload()
                    print(body)
        else:
            print("Not multipart email")
            print(parsed_email.get_payload())

        return subject, body, sender


if __name__ == "main":
    '''
    Start mail server

    SLEEPTIME defines the waiting time between server_connection
    '''
    print("Start mail serves")
    SLEEPTIME = 10

    while(True):
        server = connect()
        print("Mail:",server.stat()[0],"emails")
        print("Size:",server.stat()[1],"bytes")

        # No new emails
        if (server.stat()[0] == 0):
            print("No emails")
            server.quit()
            print("Sleeping: ", SLEEPTIME)
            sleep(SLEEPTIME)
            continue

        # Get subject, body, sender from raw email
        subject, body, sender = parse_email(server)
        if (subject == None or body == None or sender == None):
            print("Error parsing emails")
        else:
            print("Finished parsing mail\nSubject: " + subject + "\nBody: '" + body + "'\nSender: "+ sender)
            payload =  {'name':"sender",
                'studentid':"32409324",
                'message':body,
                'courseid':1,
                'labelid':"test",
                'subject':subject}

            #make a POST request
            res = requests.post('http://localhost:5000/api/ticket/submit', json=payload)
            print("RESPONSE!!")
            print(res)

        # Somehow makes you up-to-date with server
        # disable this when debugging
        server.quit()

        print("Sleeping: ", SLEEPTIME)
        sleep(SLEEPTIME)
