from controller import participants as participants_ct 
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user


participants_bp = Blueprint('participants', __name__)

@participants_bp.route("/events/<id_event>/participants", methods=["GET"])
def get_participants_by_events(id_event=None):
  if not current_user.is_authenticated:
    flash('please login')
    return redirect(url_for('index'))
  if not current_user.role == 'dosen':
    flash('you dont have access')
    return redirect(url_for('index'))
  data, title = participants_ct.get_participants_by_events(str(id_event))
  return render_template('participants/get_participants_by_event.html', data=data, title=title)

@participants_bp.route("/ep/<id_ep>/bimbingan", methods=["GET"])
def get_bimbingan_by_ep(id_ep=None):
  if not current_user.is_authenticated:
    flash('please login')
    return redirect(url_for('index'))
  data, event, ok = participants_ct.get_bimbingan_by_ep(str(id_ep))
  if not ok:
    flash('you dont have access')
    return redirect('/supervisors')
  return render_template('participants/get_bimbingan_by_ep.html', data=data, event=event)