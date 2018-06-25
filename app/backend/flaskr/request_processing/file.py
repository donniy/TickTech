from flask import Flask
from flask_hashfs import FlaskHashFS
from os.path import expanduser
import os
import uuid
import io


MAX_SIZE = 10485760


def save_file(file, file_names):

    # Setup the filesystem
    app = Flask(__name__)
    fs = FlaskHashFS()

    extension = '.' + file.filename.rsplit('.', 1)[1].lower()
    address = fs.put(file, extension=extension)
    file_names.append(File(file_id=uuid.uuid4(),
                           file_location=address.relpath,
                           file_name=file.filename,
                           is_duplicate=address.is_duplicate))

    size = os.stat(expanduser("~") + '/serverdata/' + address.relpath).st_size
    if size > MAX_SIZE:
        return False
    return True


def save_file_from_mail(bytes, filename, file_names):
    # Setup the filesystem
    app = Flask(__name__)
    fs = FlaskHashFS()
    file = io.BytesIO(bytes)
    extension = '.' + filename.rsplit('.', 1)[1].lower()
    address = fs.put(file, extension=extension)
    file_names.append(File(file_id=uuid.uuid4(),
                           file_location=address.relpath,
                           file_name=filename,
                           is_duplicate=address.is_duplicate))

    size = os.stat(expanduser("~") + '/serverdata/' + address.relpath).st_size
    if size > MAX_SIZE:
        return False
    return True


def get_file(address):

    # Download a file by address
    app = Flask(__name__)
    fs = FlaskHashFS()
    fileio = fs.open(address)

    if fileio:
        return fileio.read()
    else:
        return Iresponse.create_response("File not found", 404)


def remove_file(file):

    # Setup the filesystem
    app = Flask(__name__)
    fs = FlaskHashFS()

    # fs delete a file.
    if not file.is_duplicate:
        return fs.delete(file.file_location)
