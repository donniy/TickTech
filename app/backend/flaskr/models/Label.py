from flaskr import database, plugins
from flaskr.models.user import User
from sqlalchemy_utils import UUIDType

db = database.db


class Label(db.Model):
    """
    A Label class which specifies the label model.
    """

    __tablename__ = 'label'
    label_id = db.Column(UUIDType(binary=False), default=0, nullable=False,
                         primary_key=True)

    course_id = db.Column(UUIDType(binary=False), db.ForeignKey('course.id'),
                          default=0)
    label_name = db.Column(db.Text, nullable=False, unique=False)

    plugins = db.relationship('LabelPlugin',
                              cascade='save-update, merge, delete',
                              backref='label',
                              lazy=False)
    course = db.relationship('Course', backref='labels', lazy=False)

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
            if not cp.active:
                continue
            tmp[cp.plugin] = {}
            tmp[cp.plugin]['name'] = plugins.get_plugin_name(cp.plugin)
            tmp[cp.plugin]['active'] = cp in self.plugins
            if cp in self.plugins:
                tmp[cp.plugin]['assignment_id'] = self.get_plugin(cp.plugin)\
                                                      .assignment_id

        return tmp

    def get_active_plugins(self):
        """
        Get all plugins which are active.
        """
        tmp = []
        for lp in self.plugins:
            if lp not in self.course.plugins:
                continue
            tmp.append({'id': lp.plugin, 'lp': lp})
        return tmp

    def get_tas(self, user_id):
        """
        Get the teaching assistants for this label using the plugins.
        """
        tmp = []
        for plugin in self.get_active_plugins():
            p = plugins.get_plugin(plugin['id'])
            cp = self.course.get_plugin(plugin['id'])
            ta_id = p.get_ta(cp.get_settings(),
                             user_id,
                             plugin['lp'].assignment_id)
            if ta_id:
                tmp.append(User.query.get(ta_id))
        return set(tmp)

    def get_assignment_info(self, user_id):
        """
        Get the assignment info for all plugins connected to this label.
        """
        pls = {}
        for plugin in self.get_active_plugins():
            p = plugins.get_plugin(plugin['id'])
            cp = self.course.get_plugin(plugin['id'])
            if cp.active:
                print("Getting assignment info for {}".format(plugin['id']))
                info = p.get_assignment_info(cp.get_setting_values(),
                                             user_id,
                                             plugin['lp'].assignment_id)
                if info:
                    pls[p.display_name] = info
        return pls

    def create(self, id, name, course_id):
        self.label_id = id
        self.label_name = name
        self.course_id = course_id


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
