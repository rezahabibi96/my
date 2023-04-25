from flask_login import UserMixin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
from . import db


# db = SQLAlchemy()
bc = Bcrypt()

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    username = db.Column(db.String, unique = True)
    email = db.Column(db.String, unique = True)
    role = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, id, fullname, username, email, password, role='mahasiswa'):
        self.id = id
        self.fullname = fullname
        self.username = username
        self.email = email
        self.role = role
        self.password = password

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.username)

    def save(self):    
        db.session.add(self)
        db.session.commit()
        return self

lm = LoginManager()
@lm.user_loader
def user_loader(id):
    return Users.query.get(int(id))