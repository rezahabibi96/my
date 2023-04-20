from controller import auth as auth_ct
from flask import Blueprint, request


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signout')
def signout():
    return auth_ct.signout()

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return auth_ct.signup(request)

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    return auth_ct.signin(request)