from flaskr import database
from sqlalchemy_utils import UUIDType

db = database.db

class Label(db.Model):

    """
    Een Label.
    """

    __tablename__ = 'label'
    label_id = db.Column(UUIDType(binary=False), default=0, nullable=False,
                         primary_key=True)
    label_name = db.Column(db.Text, nullable=False, unique=False)

    plugins = db.relationship('LabelPlugin', backref='label', lazy=False)

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


class LabelPlugin(db.Model):
    """
    This keeps track of an activated plugin for this label. Also stores which
    assignment is related to this label.
    """
    id = db.Column(UUIDType(binary=False), default=0, nullable=False,
                   primary_key=True)
    label_id = db.Column(UUIDType(binary=False), db.ForeignKey(
        'label.label_id'), default=0, nullable=False)
