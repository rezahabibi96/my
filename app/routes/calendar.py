from controller import calendar as calendar_ct
from flask import Blueprint, request, make_response
import sys


calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route("/get/", methods=["POST"])
def get():
  form = dict(request.form)
  data = calendar_ct.get(int(form["month"]), int(form["year"]))
  return "{}" if data is None else data

@calendar_bp.route("/save/", methods=["POST"])
def save():
  data = dict(request.form)
  ok = calendar_ct.save(data["s"], data["e"], data["t"], data["c"], data["b"], data["cat"],
                        data["id"] if "id" in data else None)
  msg = "OK" if ok else sys.last_value
  return make_response(msg, 200)

@calendar_bp.route("/cut/", methods=["POST"])
def cut():
  data = dict(request.form)
  ok = calendar_ct.cut(data["id"])
  msg = "OK" if ok else sys.last_value
  return make_response(msg, 200)