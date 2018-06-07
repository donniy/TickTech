from flask import Blueprint

apiBluePrint = Blueprint("api", __name__, url_prefix="/api")

<<<<<<< HEAD
from . import course, ticket, user
=======
from . import course, ticket, user, CourseOverview
>>>>>>> master
