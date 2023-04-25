from . import db


class Tendik(db.Model):

    __tablename__ = 'tendik'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tendik = db.Column(db.Integer, db.ForeignKey('users.id'))
    bagian = db.Column(db.String)

    def __init__(self, id_tendik, bagian='NULL'):
        self.id_tendik = id_tendik
        self.bagian = bagian

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.id_tendik)

    def save(self):    
        db.session.add(self)
        db.session.commit()
        return self