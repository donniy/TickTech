from flask_mail import Message


def create_email_message(title, recipients, ticketid, body, sender, timestamp):
    print("Sending message to: " + recipients[0] + "Message says: " + body)
    message = Message(title, recipients=recipients)
    message.body = ("You got a new message on ticket: " + ticketid
                    + "\nFrom:" + sender + "\n\n\n" + body
                    + "\n\nMessage was send on: " + timestamp)
    return message
