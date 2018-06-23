from flask_jwt_extended import get_jwt_identity
from flaskr.models import user


def get_current_user():
    curr_id = get_jwt_identity()
    if curr_id is None:
        return None
    return user.User.query.get(curr_id)
