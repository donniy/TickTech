from flask_mail import Message

def create_email_message(title, recipients, ticketid, body, sender):
    message = Message(title, recipients=recipients)
    message.html = (
        '<body>You got a new message ' +
        '<a href="http://localhost:5000/ticket/' + ticketid +
        '">Your ticket</a><br />' +
        'From: ' + sender + '<hr><br />' + body +
        '</body>'
    )
    return message
