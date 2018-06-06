from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path


db = SQLAlchemy()

def init_db():
    db.create_all()
    addTicketStatus()
    addTicket()


def json_list(l):
    """
    Maak JSON van de lijst.
    """
    return jsonify(json_list=[i.serialize for i in l])


#just for testing
def addTicketStatus(name="Needs help"):
    from flaskr.models import ticket
    ts = ticket.TicketStatus()
    ts.name = name
    db.session.add(ts)
    db.session.commit()


def addTicketLabel(ticked_id=1, course_id="1", name="test"):
    from flaskr.models import ticket
    tl = ticket.TicketLabel()
    tl.ticked_id = ticked_id
    tl.course_id = course_id
    tl.name = name
    db.session.add(tl)
    db.session.commit()


#just for testing
def addTicket(user_id=1, email="test@email.com", course_id="1", status_id=1, title="test",
              timestamp=datetime.now()):
    from flaskr.models import ticket
    t = ticket.Ticket()
    addTicketLabel(t.id, course_id, title)
    t.user_id = user_id
    t.email = email
    t.course_id = course_id
    t.status_id = status_id
    t.title = title
    t.timestamp = timestamp
    t.label_id = 1
    db.session.add(t)
    db.session.commit()
