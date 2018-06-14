from flaskr import database
from flaskr.models.Course import *

db = database.db


class User(db.Model):

    """
    Een user.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, nullable=False, primary_key=True)  # student ID
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)

    # Dit is een soort toString zoals in Java, voor het gebruiken van de
    # database in de commandline. Op die manier kan je data maken en weergeven
    # zonder formulier.
    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def serialize(self):
        """
        Zet de user om in json. Dit is alles wat de frontend kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }

    @property
    def checkValid(self):
        """
        Niet nodig.
        """
        pass
