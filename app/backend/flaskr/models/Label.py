from flaskr import database, plugins
from sqlalchemy_utils import UUIDType

db = database.db

class Label(db.Model):
    """
    Een Label.
    """

    __tablename__ = 'label'
    label_id = db.Column(UUIDType(binary=False), default=0, nullable=False,
                         primary_key=True)

    course_id = db.Column(UUIDType(binary=False), db.ForeignKey('course.id'),
                          default=0)
    label_name = db.Column(db.Text, nullable=False, unique=False)

    plugins = db.relationship('LabelPlugin', backref='label', lazy=False)
    course = db.relationship('Course', backref='labels', lazy=False)

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

    def get_plugin(self, plugin_id):
        """
        Get the plugin with given plugin id.
        """
        for lp in self.plugins:
            if lp.plugin == plugin_id:
                return lp
        return None

    def get_plugins(self):
        """
        Get all (available) plugins for this label along with their active
        state and assignment_id.
        """
        tmp = {}
        for cp in self.course.plugins:
            tmp[cp.plugin] = {}
            tmp[cp.plugin]['name'] = plugins.get_plugin_name(cp.plugin)
            tmp[cp.plugin]['active'] = cp in self.plugins
            if cp in self.plugins:
                tmp[cp.plugin]['assignment_id'] = self.get_plugin(cp.plugin)\
                                                      .assignment_id

        return tmp


class LabelPlugin(db.Model):
    """
    This keeps track of an activated plugin for this label. Also stores which
    assignment is related to this label.
    """
    id = db.Column(UUIDType(binary=False), default=0, nullable=False,
                   primary_key=True)
    label_id = db.Column(UUIDType(binary=False), db.ForeignKey(
        'label.label_id'), default=0, nullable=False)
    plugin = db.Column(db.String(255), unique=False, nullable=False)
    assignment_id = db.Column(db.String(255), nullable=False)

    def __eq__(self, other):
        """
        Compare two plugins.
        """
        return self.plugin == other.plugin
