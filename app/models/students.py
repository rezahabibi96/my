from . import db


class Students(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_student = db.Column(db.Integer, db.ForeignKey('users.id'))
    semester = db.Column(db.String)

    def __init__(self, id_student, semester='NULL'):
        self.id_student = id_student
        self.semester = semester

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.id_student)

    def save(self):    
        db.session.add(self)
        db.session.commit()
        return self