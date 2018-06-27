import re


def validate_userdata(email, name, studentid, password, repassword):
    # Check email.
    regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    if not regex.match(email):
        return "Invalid email address"

    if not len(name) >= 1:
        return "No name provided"

    if not password == repassword:
        return "Passwords did not match"

    if studentid < 10000 or studentid > 100000000:
        return "Invalid student ID"

    return ''
