from flaskr import database

db = database.db
# courses_helper = db.Table(
#     'courses',
#     db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True), #klopt dit?
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

class User(db.Model):
    """
    Een user.
    """
    id = db.Column(db.Integer, nullable=False, primary_key=True) # student ID
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    
    # Many to many relation
    # courses = db.relationship( 
        # "UserCourses", secondary=courses_helper, lazy='subquery',
        # backref=db.backref('courses', lazy=True))

    # Dit is een soort toString zoals in Java, voor het gebruiken van de database
    # in de commandline. Op die manier kan je data maken en weergeven zonder formulier.
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
            'user_id': self.user_id,
            'email': self.email,
            'courses': database.serialize_list(self.courses)
        }

    @property
    def checkValid(self):
        """
        Niet nodig.
        """
        pass
