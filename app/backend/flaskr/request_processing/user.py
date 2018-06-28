import re
from flaskr import database, Iresponse
from datetime import datetime, timedelta
import uuid
import bcrypt
from flaskr.models.user import User
from mail.Message import changePassword
from flask_mail import Mail
from threading import Thread
from flask import current_app
from flask import escape

def validate_userdata(email, name, studentid, password, repassword):
    # Check email.
    regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    if not regex.match(email):
        return "Invalid email address"

    if not len(name) >= 1:
        return "No name provided"

    if not password == repassword:
        return "Passwords did not match"

    print(studentid)
    if studentid < 10000 or studentid > 1000000000:
        return "Invalid student ID"

    return ''


def register_user(json_data):
    email = escape(json_data["email"])
    name = escape(json_data["name"])
    studentid = int(escape(json_data["studentid"]))
    password = escape(json_data["password"])
    repassword = escape(json_data["password_confirmation"])

    validated = validate_userdata(email, name, studentid, password, repassword)
    if validated != '':
        return Iresponse.create_response({"status": validated}, 200)

    # Backend check if email/studentid already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return Iresponse.create_response({"status": "Email is taken"}, 200)

    studentid = json_data["studentid"]
    user = User.query.filter_by(id=studentid).first()

    if user:
        return Iresponse.create_response({"status": "Studentid taken"}, 200)

    new_user = User()
    salt = bcrypt.gensalt()
    hashedpsw = bcrypt.hashpw(password.encode('utf-8'), salt)
    new_user.password = hashedpsw
    new_user.id = studentid
    new_user.name = name
    new_user.email = email
    new_user.level = 1
    new_user.experience = 1

    if not database.addItemSafelyToDB(new_user):
        return Iresponse.internal_server_error()

    return Iresponse.create_response({"status": "OK"}, 201)

def reset_password(json_data):
    password = json_data["password"]
    psw_confirmation = json_data["psw_confirmation"]
    code = json_data["code"]

    if password == psw_confirmation:
        user = User.query.filter_by(code=code).first()
        if user:
            if user.code_expiration:
                present = datetime.now()
                if user.code_expiration < present:
                    if user.code:
                        if user.code == uuid.UUID(code):
                            salt = bcrypt.gensalt()
                            hashedpsw = bcrypt.hashpw(password.encode('utf-8'),
                                                      salt)
                            user.password = hashedpsw
                            user.code = None
                            user.code_expiration = None
                            database.db.session.commit()
                            return Iresponse.create_response("Succes", 200)
                        else:
                            print(code, user.code)
                            return Iresponse.create_response("Wrong code", 403)
                    else:
                        return Iresponse.create_response("No code", 403)
                else:
                    return Iresponse.create_response("Code expired", 403)
            else:
                return Iresponse.create_response("Can't reset", 403)
        else:
            return Iresponse.create_response("Invalid code", 404)
    else:
        return Iresponse.create_response("Passwords don't match", 403)

def set_reset_code(email):

    user_data = User.query.filter_by(email=email).first()
    present = datetime.utcnow()

    if not user_data:
        return Iresponse.create_response("No user found by this email", 200)

    if user_data.code_expiration is None or user_data.code_expiration < present:
        user_data.code = uuid.uuid4()
        user_data.code_expiration = present + timedelta(0, 7200)
        database.db.session.commit()

        message = changePassword([user_data.email], str(user_data.code))
        app = current_app._get_current_object()
        thr = Thread(target=send_async_email, args=[message, app])
        thr.start()
        return Iresponse.create_response(str(user_data.code), 201)


    return Iresponse.create_response("Your previous link hasn't expired", 200)

def send_async_email(message, app):
    with app.app_context():
        Mail().send(message)
