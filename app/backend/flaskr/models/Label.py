from flaskr import database
from sqlalchemy_utils import UUIDType

db = database.db


class Label(db.Model):

    """
    A Label class which specifies the label model.
    """

    __tablename__ = 'label'
    label_id = db.Column(UUIDType(binary=False), default=0, nullable=False,
                         primary_key=True)
    label_name = db.Column(db.Text, nullable=False, unique=False)

    @property
    def serialize(self):
        """
        Transforms the object into a json object.
        This will be used at the front-end, so dont include
        sensitive information in the json object.
        """
        return {
            'label_id': self.label_id,
            'label_name': self.label_name,
        }
