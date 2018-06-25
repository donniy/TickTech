import re


def validate_userdata(email, name, studentid, password, repassword):
    # Check email.
    regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    if not regex.match(email):
        return False

    if not len(name) >= 2:
        return False

    if not password == repassword and len(password) < 5:
        return False

    if studentid < 10000 or studentid > 100000000:
        return False

    return True
