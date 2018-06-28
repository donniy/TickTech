from flask_mail import Message


def createdTicketEmail(title, recipients, ticketid, body):
    '''
    Sends an email to the student, confirming we received their email
    and created a ticket on TIKTECH. The ticket id is in the subject.
    '''
    string = "TIKTECH Confirmation: " + title + ". Ticket ID: " + ticketid
    message = Message(subject=string, recipients=recipients)
    message.html = (
        '<body>Hey!<br />We received your e-mail and created ' +
        'a matching ticket on TIKTECH.' +
        '<br /> Check it out ' +
        '<a href="http://localhost:5000/login?redirect=' + ticketid +
        '">here</a>.<br /> Please note that this is an automatically ' +
        'generated e-mail.' +
        'Please do not reply here, but contact your TAs if necessary.' +
        '<hr><br /><br />Your e-mail:' + body + '</body>'
    )

    return message


def createdEmailMessage(title, recipients, ticketid, body, sender):
    '''
    Sends an email to the student, confirming a TA has responded
    to their ticket on TIKTECH (e.g. a message has been added to the ticket).
    '''
    string = "TIKTECH notification. Ticket ID: " + ticketid
    message = Message(subject=string, recipients=recipients)
    message.html = (
        '<body>Hey!<br />You got a new reply to your question from ' + sender +
        '.<br /> Check out your ' +
        '<a href="http://localhost:5000/login?redirect=' + ticketid +
        '">ticket</a> at TIKTECH.<br /> ' +
        '<hr><br />' + body + '</body>'
    )

    return message


def ticketErrorEmail(title, recipients, body):
    '''
    Sends an email to the student, confirming we received their email
    but an error occurred when adding it to TIKTECH.
    '''
    string = "TIKTECH error. We could not process: " + title
    message = Message(subject=string, recipients=recipients)
    message.html = (
        '<body>Hey!<br />We received your e-mail, but encountered an ' +
        'error while processing it in our database.<br /> ' +
        'Please resent it and clearly state your student ID ' +
        'in the following format on a separate line: <br /><br />' +
        'student ID = [your student ID here]. <br /><br />' +
        'If you already did this, please do not reply here,' +
        'but contact your TAs if necessary. <hr><br />' +
        'Your original e-mail: <br />' + body + '</body>'
    )

    return message


def replyErrorEmail(title, recipients, ticketid, body):
    '''
    Sends an email to the student, confirming we received their email
    as a reply on an original ticket,
    but an error occurred when adding it to TIKTECH.
    '''
    string = "TIKTECH error. We could not process your reply: " + title
    message = Message(subject=string, recipients=recipients)
    message.html = (
        '<body>Hey!<br />We received your e-mail, but encountered an' +
        'error while processing it in our database.<br /> ' +
        'Please resent it or visit your original' +
        '<a href="http://localhost:5000/login?redirect=' + ticketid +
        '">ticket</a> and reply there.<br />' +
        'Please do not reply here, but contact your TAs if necessary.' +
        'Your original e-mail:' + body + '</body>')
    return message


def somethingWentWrong(title, recipients, part, body):
    '''
    It went wrong somewhere:
    '''
    string = "TIKTECH error. We could not process: " + title
    string = string.replace('\n', '')
    message = Message(subject=string, recipients=recipients)
    message.html = (
        '<body> We received your e-mail, but encountered an' +
        'error while processing.<br /> ' +
        'error message: \"' + part + '\"<br /><br />' +
        'Please resent it or contact your TA' +
        'Please do not reply to this e-mail.' +
        'Your original e-mail:' + body + '</body>'
    )
    return message
