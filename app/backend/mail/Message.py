from flask_mail import Message

def createEmailMessage(title, recipients, ticketid, body, sender):
    '''
    #TODO:
    '''
    message = Message(subject=title, recipients=recipients)
    message.html = (
        '<body>You got a new reply to your question from ' + sender +
        '.<br /> Check out your ' +
        '<a href="http://localhost:5000/login?test=' + ticketid +
        '">ticket</a> at TIKTECH.<br /> ' +
        '<hr><br />' + body + '</body>'
    )
    return message


def createdTicketEmail(title, recipients, ticketid, body):
    '''
    #TODO:
    '''

    message = Message(
        subject="TIKTECH Confirmation:" + title + ". Ticket ID: " +  ticketid, recipients=recipients)
    message.html = ('<body> We received your e-mail and created a matching ticket on TIKTECH.' +
                    '.<br /> Check it out ' +
                    '<a href="http://localhost:5000/login?test=' + ticketid +
                    '">here</a>.<br /> This is an automatically generated e-mail.' +
                    'Please do not reply here. <hr><br /> Your e-mail:' + body + '</body>'
                    )
    return message


def ticketErrorEmail(title, recipients, body):
    '''
    #TODO:
    '''
    message = Message(
        subject="TIKTECH error. We could not process: " + title, recipients=recipients)
    message.html = ('<body> We received your e-mail, but encountered an error while processing.' +
                    '.<br /> Please resent it and clearly state your student ID '+
                    'in the following format on a separate line: <br /><br />' +
                    'student ID = [your student ID here]. <br /><br />' +
                    'If you already did this, please contact your TA. <br />'
                    'Please do not reply to this e-mail. <hr><br />' +
                    'Your original e-mail: <br />' + body + '</body>'
                    )
    return message

# TODO: Dit invoeren.
def replyErrorEmail(title, recipients, ticketid, body):
    '''
    #TODO:
    '''
    message = Message(
        subject="TIKTECH error. We could not process: " + title, recipients=recipients)
    message.html = ('<body> We received your e-mail, but encountered an' +
                    'error while processing.<br /> ' +
                    'Please resent it or visit your original' +
                    '<a href="http://localhost:5000/login?test=' + ticketid +
                    '">ticket</a> and reply there.<br />' +
                    'Please do not reply to this e-mail.' +
                    'Your original e-mail:' + body + '</body>'
                    )
    return message
