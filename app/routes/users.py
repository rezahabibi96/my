from controller import users as users_ct
from flask import Blueprint, request, make_response, render_template, redirect, url_for
from flask_login import current_user, login_required


users_bp = Blueprint('users', __name__)

@users_bp.route("/users/profile", methods=["GET"])
def get_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    print(current_user.password, 'aa')
    return {'a': 'a'}
    
    data =  users_ct.get_profile()
    return render_template('users/profile.html', data=data)