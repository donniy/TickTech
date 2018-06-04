from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")
# Deze database is een tijdelijke sqlite database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

def json_list(l):
    """
    Maak JSON van de lijst.
    """
    return jsonify(json_list=[i.serialize for i in l])

class Ticket(db.Model):
    """
    Een ticket.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    course_id = db.Column(db.String(120), unique=False, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('ticket_status.id'), default=0, nullable=False)
    title = db.Column(db.String(255), unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Dit is hoe je een relatie maakt. ticket.status geeft een TicketStatus object met
    # de status van dit ticket. backref betekent: maak een veld 'tickets' op TicketStatus
    # wat een lijst met alle tickets met die status teruggeeft.
    status = db.relationship('TicketStatus', backref=db.backref('tickets', lazy=True))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de database
    # in de commandline. Op die manier kan je data maken en weergeven zonder formulier.
    def __repr__(self):
        return '<Ticket {}>'.format(self.title)
    
    @property
    def serialize(self):
        """
        Zet dit ticket om in json. Dit is alles wat de front-end kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'title': self.title,
            'course_id': self.course_id,
            'status': self.status.serialize,
        }

class TicketStatus(db.Model):
    """
    De status van een ticket die kan worden ingesteld.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


@app.route('/api/course/<course_id>')
def retrieve_course_tickets(course_id):
    """
    Geeft alle ticktes over gegeven course.
    """
    # TODO: Controleer of degene die hierheen request permissies heeft.
    tickets = Ticket.query.filter_by(course_id=course_id).all()
    return json_list(tickets)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def render_vue(path):
    return render_template("index.html")

