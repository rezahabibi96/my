from . import db


class Hima(db.Model):

    __tablename__ = 'hima'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_hima = db.Column(db.Integer, db.ForeignKey('users.id'))
    divisi = db.Column(db.String)

    def __init__(self, id_hima, divisi='NULL'):
        self.id_hima = id_hima
        self.divisi = divisi

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.id_hima)

    def save(self):    
        db.session.add(self)
        db.session.commit()
        return self