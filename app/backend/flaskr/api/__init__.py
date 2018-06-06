from flask import Blueprint

apiBluePrint = Blueprint("api", __name__, url_prefix="/api")

from . import course, ticket, CourseOverview, Notes
