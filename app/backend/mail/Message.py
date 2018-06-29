from flask_mail import Message


def createdTicketEmail(title, recipients, ticketid, body):
    '''
    Sends an email to the student, confirming we received their email
    and created a ticket on TIKTECH. The ticket id is in the subject.
    '''
    subject = "TIKTECH Confirmation: " + title + ". Ticket ID: " + ticketid
    message = Message(subject=subject, recipients=recipients)
    message.html = (
        '<body>Hey!<br />We received your email and created ' +
        'a matching ticket on TIKTECH.' +
        '<br /> Check it out ' +
        '<a href="http://localhost:5000/login?redirect=' + ticketid +
        '">here</a>.<br /> Please note that this is an automatically ' +
        'generated email.' +
        'Please do not reply here, but contact your TAs if necessary.' +
        '<hr><br /><br />Your email:' + body + '</body>'
    )

    return message


def createdEmailMessage(title, recipients, ticketid, body, sender):
    '''
    Sends an email to the student, confirming a teaching assistant has responded
    to their ticket on TIKTECH (e.g. a message has been added to the ticket).
    '''
    subject = "TIKTECH Notification. Ticket ID: " + ticketid
    message = Message(subject=subject, recipients=recipients)
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
    subject = "TIKTECH error. We could not process: " + title
    message = Message(subject=subject, recipients=recipients)
    message.html = (
        '<body>Hey!<br />We received your email, but encountered an ' +
        'error while processing it in our database.<br />' +
        'Please resent it and clearly state your student ID ' +
        'in the following format on a separate line: <br /><br />' +
        'student ID = [your student ID here]. <br /><br />' +
        'If you already did this, please do not reply here,' +
        'but contact your TAs if necessary. <hr><br />' +
        'Your original email: <br />' + body + '</body>'
    )

    return message


def replyErrorEmail(title, recipients, ticketid, body):
    '''
    Sends an email to the student, confirming we received their email
    as a reply on an original ticket,
    but an error occurred when adding it to TIKTECH.
    '''
    subject = "TIKTECH error. We could not process your reply: " + title
    message = Message(subject=subject, recipients=recipients)
    message.html = (
        '<body>Hey!<br />We received your email, but encountered an' +
        'error while processing it in our database.<br />' +
        'Please resent it or visit your original' +
        '<a href="http://localhost:5000/login?redirect=' + ticketid +
        '">ticket</a> and reply there.<br />' +
        'Please do not reply here, but contact your TAs if necessary.' +
        'Your original email:' + body + '</body>')
    return message


def somethingWentWrong(title, recipients, part, body):
    '''
    Sends an email to the student, confirming we received their email,
    but notifying them that it went wrong somewhere, and an appropriate
    error message is displayed.
    '''
    subject = "TIKTECH error. We could not process: " + title
    subject = subject.replace('\n', '')
    message = Message(subject=subject, recipients=recipients)
    message.html = (
        '<body>Hey!<br />We received your email, but encountered an' +
        'error while processing it in our database.<br />' +
        'The error message: \"' + part + '\"<br /><br />' +
        'Please resent your email or contact your TA.' +
        'Please do not reply to this automatically generated email.' +
        'Your original email:' + body + '</body>'
    )
    return message


def changePassword(recipients, linkid):
    message = Message(
        subject="Change password",
                recipients=recipients)
    message.html = (
        '<body style="margin: 0; padding: 0;">' +
        '<table border="1" cellpadding="0" cellspacing="0" width="100%">' +
        '<td>' +
        '<tr>' +
        'With this link you can reset your password for the next' +
        ' 2 hours. Please do not share it with others.<br /><br />' +
        'Please reset your password with the follow link: ' +
        '<a href="http://localhost:5000/resetpassword?code=' +
        linkid + '">reset password</a>' +
        '</td>' +
        '</tr>' +
        '</table>' +
        '<p>&copy; 2018 Tiktech<p>' +
        '</body>')
    return message
