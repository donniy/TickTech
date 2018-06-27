from flaskr import database, Iresponse
from math import floor
from flaskr.models.user import User
from flaskr.models.Message import Message
from flaskr.models.ticket import Ticket
from flaskr.models.Course import Course
from flaskr.utils import notifications
import datetime


EXP_FOR_ASSING = 20
EXP_FOR_MENTION = 40
EXP_FOR_RESPONSE = 150
EXP_FOR_NOTE = 30
EXP_FOR_CLOSE = 80


def equate(xp):
    xp_max = xp + 300
    factor = xp / 7.0
    mult_2 = 2 ** factor
    end = xp_max * mult_2
    return floor(end)


def level_to_xp(level):
    totalxp = 0

    for lvl in range(1, level):
        totalxp += equate(lvl)
    return floor(totalxp / 4)


def xp_to_level(xp):
    level = 1

    while level_to_xp(level) < xp:
        level += 1

    return level


def add_experience(experience, user_id):
    user = User.query.get(user_id)
    weekno = datetime.datetime.today().weekday()

    if weekno >= 5:
        experience *= 2

    if not user:
        return None
    experience = user.experience + experience
    retval = 0
    new_level = xp_to_level(experience)
    if new_level > user.level:
        retval = new_level - user.level
        user.level = new_level
    user.experience = experience
    database.db.session.commit()

    return retval


def deduct_experience(experience, user_id):
    user = User.query.get(user_id)

    if not user:
        return None
    experience = user.experience + experience
    retval = 0
    new_level = xp_to_level(experience)
    if new_level < user.level:
        retval = new_level - user.level
        user.level = new_level
    user.experience = experience
    database.db.session.commit()

    return retval


def notify_level_change(user_id, ticket, level_up):
    if ticket:
        course = Course.query.get(ticket.course_id)
    else:
        course = None
    user = User.query.get(user_id)
    if user in course.ta_courses or course is None:
        try:
            if level_up == 1:
                notification = notifications.notify(user_id,
                                                    ticket,
                                                    "gained a level!",
                                                    Message.NTFY_LVL_UP)
            elif level_up > 1:
                notify_msg = "gained " + str(level_up) + " levels!"
                notification = notifications.notify(user_id,
                                                    ticket,
                                                    notify_msg,
                                                    Message.NTFY_LVLS_UP)
            elif level_up == -1:
                notification = notifications.notify(user_id,
                                                    ticket,
                                                    "",
                                                    Message.NTFY_LVL_DWN)
            elif level_up == -1:
                notification = notifications.notify(user_id,
                                                    ticket,
                                                    "",
                                                    Message.NTFY_LVLS_DWN)
        except Exception as e:
            return None
