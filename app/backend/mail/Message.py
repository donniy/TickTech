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

# Metadata toevoegen aan een email om replies aan een ticket hangen.
# Parsen op ticket id in subject
# (Welk ticket reply je op? - dat moet een message worden, niet een nieuw ticket)
# Kijk of de user bij de ticket hoort
