from utils import database as init_db, populate as init_populate
from models import users as users_md
from routes import calendar as calendar_rt, auth as auth_rt, events as events_rt, users as users_rt
from routes import supervisors as supervisors_rt, participants as participants_rt, searchs as searchs_rt 
from flask import Flask, render_template, flash


HOST_NAME = "localhost"
HOST_PORT = 80
app = Flask(__name__)
# app.debug = True

app.config.from_object('utils.config.Config')

users_md.lm.init_app(app)
users_md.db.init_app(app)
users_md.bc.init_app(app)

app.register_blueprint(calendar_rt.calendar_bp)
app.register_blueprint(auth_rt.auth_bp)
app.register_blueprint(events_rt.events_bp)
app.register_blueprint(users_rt.users_bp)
app.register_blueprint(supervisors_rt.supervisors_bp)
app.register_blueprint(participants_rt.participants_bp)
app.register_blueprint(searchs_rt.searchs_bp)

@app.route("/", methods=["GET", "POST"])
def index():
  return render_template("index.html")

@app.route("/index", methods=["GET"])
def root():
  return "myDSB kompetisi"

@app.before_first_request
def initialize_config():
  # init_db.init()
  # init_populate.init(app)
  pass
  pass

if __name__ == "__main__":
  app.run(HOST_NAME, HOST_PORT, debug=True) 