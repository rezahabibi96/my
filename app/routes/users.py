from controller import users as users_ct
from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response
from flask_login import current_user, login_required


users_bp = Blueprint('users', __name__)

@users_bp.route("/users/home", methods=["GET"])
def get_home():
    if not current_user.is_authenticated:
        flash('please login')
        return redirect(url_for('index'))
    
    data =  users_ct.get_home()
    return render_template('users/home.html', data=data)

@users_bp.route("/users/profile", methods=["GET", "POST"])
@users_bp.route("/users/profile/edit", methods=["GET", "POST"])
def get_profile():
    if not current_user.is_authenticated:
        flash('please login')
        return redirect(url_for('index'))
    
    return users_ct.get_profile(request)

@users_bp.route("/users/password", methods=["GET", "POST"])
def get_password():
    if not current_user.is_authenticated:
        flash('please login')
        return redirect(url_for('index'))
    
    return users_ct.get_password(request)

@users_bp.route("/users/students", methods=["GET"])
def get_mystudents():
  if not current_user.is_authenticated:
    flash('please login')
    return redirect(url_for('index'))
  if not current_user.role == 'mahasiswa':
    flash('you dont have access')
    return redirect(url_for('index'))
  data = users_ct.get_mystudents()
  return render_template('users/mystudents.html', data=data)

@users_bp.route("/users/competitions", methods=["GET", "POST"])
def get_mycompetitions():
  if not current_user.is_authenticated:
    flash('please login')
    return redirect(url_for('index'))
  if not current_user.role == 'dosen':
    flash('you dont have access')
    return redirect(url_for('index'))  
  data = users_ct.get_mycompetitions()
  return render_template('users/mycompetitions.html', data=data)