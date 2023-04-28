from controller import supervisors as supervisors_ct
from flask import Blueprint, render_template


supervisors_bp = Blueprint('supervisors', __name__)

@supervisors_bp.route("/supervisors/<id_supervisor>", methods=["GET"])
def get_supervisor(id_supervisor=None):
  supervisors_ct.get_supervisor(id_supervisor)
  return render_template('supervisors/get_supervisor.html', id_supervisor)

@supervisors_bp.route("/supervisors", methods=["GET"])
def get_supervisors():
  data = supervisors_ct.get_supervisors()
  return render_template('supervisors/get_supervisors.html', data=data)