from flask_mail import Message


def createEmailMessage(title, recipients, ticketid, body, sender):
    message = Message(subject="RE: " + title, recipients=recipients)
    message.html = (
        '<body>You got a new reply to your question from ' + sender +
        '.<br /> Check out your ' +
        '<a href="http://localhost:5000/ticket/' + ticketid +
        '">ticket</a> at TIKTECH.<br /> ' +
        '<hr><br />' + body + '</body>'
    )
    return message


# DIT OOK NOG
def createdTicketEmail(title, recipients, ticketid, body):
    message = Message(
        subject="TIKTECH Confirmation. Received your question: " + title, recipients=recipients)
    message.html = ('<body> We received your e-mail and created a matching ticket on TIKTECH.' + 
                    '.<br /> Check it out ' +
                    '<a href="http://localhost:5000/ticket/' + ticketid +
                    '">here</a>.<br /> This is an automatically generated e-mail.' +
                    'Please do not reply here. <hr><br /> Your e-mail:' + body + '</body>'
                    )
    return message


# DIT FAALT
def ticketErrorEmail(title, recipients, body):
    message = Message(
        subject="TIKTECH error. We could not process: " + title, recipients=recipients)
    message.html = ('<body> We received your e-mail, but received an error while processing.' + 
                    '.<br /> Please resent it and clearly state your student ID'+ 
                    'in the following format on a separate line: <br />' +
                    'student ID = [your student ID here] <br />' + 
                    'Please do not reply to this e-mail. Alternatively, contact your TA. <hr><br />' +
                    'Your originel e-mail:' + body + '</body>'
                    )
    return message


# Metadata toevoegen aan een email om replies aan een ticket hangen.
# Parsen op ticket id in subject
# (Welk ticket reply je op? - dat moet een message worden, niet een nieuw ticket)
# Kijk of de user bij de ticket hoort
