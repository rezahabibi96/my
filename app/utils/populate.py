from models import users as users_md, lecturers as lecturers_md, hima as hima_md, tendik as tendik_md
from .config import Config
import json
  

JSON = Config.JSON

def init(app):
    with open(JSON) as f:
        data = json.load(f)
        
        with app.app_context():
            for user in data["users"]:
                password = users_md.bc.generate_password_hash(user['password'])
                user = users_md.Users(user['id'], user['fullname'], user['username'], user['email'], password, user['role'])
                user.save()

            for lecturer in data["lecturers"]:
                lecturer = lecturers_md.Lecturers(lecturer['id_lecturer'], lecturer['research_interest'])
                lecturer.save()

            for hima in data["hima"]:
                hima = hima_md.Hima(hima['id_hima'], hima['divisi'])
                hima.save()

            for tendik in data["tendik"]:
                tendik = tendik_md.Tendik(tendik['id_tendik'], tendik['bagian'])
                tendik.save()

        print('data populated')