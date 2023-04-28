from . import db


class Lecturers(db.Model):

    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_lecturer = db.Column(db.Integer, db.ForeignKey('users.id'))
    research_interest = db.Column(db.String)
    research_group = db.Column(db.String)

    def __init__(self, id_lecturer, research_interest='NULL', research_group='NULL'):
        self.id_lecturer = id_lecturer
        self.research_interest = research_interest
        self.research_group = research_group

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.id_lecturer)

    def save(self):    
        db.session.add(self)
        db.session.commit()
        return self