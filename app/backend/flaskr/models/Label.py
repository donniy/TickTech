from datetime import datetime
from flaskr import database
from sqlalchemy_utils import UUIDType

db = database.db


class Label(db.Model):
    """
    Een Label.
    """
    label_id = db.Column(UUIDType(binary=False), default=0, nullable=False, primary_key=True)
    label_name = db.Column(db.Text, nullable=False, unique=False)

    @property
    def serialize(self):
        """
        Zet de message om in json. Dit is alles wat de front-end kan zien,
        dus zorg dat er geen gevoelige info in zit.
        """
        return {
            'label_id': self.label_id,
            'label_name': self.label_name,
        }

    @property
    def checkValid(self):
        pass
