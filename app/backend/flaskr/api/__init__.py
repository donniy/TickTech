from flask import Blueprint
from . import course, ticket, user, login, notes, ta, labels, mail

apiBluePrint = Blueprint("api", __name__, url_prefix="/api")
