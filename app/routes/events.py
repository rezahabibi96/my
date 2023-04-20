from controller import events as events_ct
from flask import Blueprint, request, make_response, render_template


events_bp = Blueprint('events', __name__)

@events_bp.route("/events/<id_event>", methods=["GET"])
def get_event(id_event=None):
  data = events_ct.get_event(str(id_event))
  return render_template('events/get_event.html', data=data)