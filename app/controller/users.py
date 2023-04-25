from models import users as users_md
from utils.config import Config
from flask import render_template, flash, redirect
from flask_login import current_user, login_required
import requests
import sqlite3
import random
import json


DB = Config.DB

def get_home():
    # conn = sqlite3.connect(DB)
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM `events` WHERE (`id` = ?)", (1,))
    # user = cursor.fetchone()
    # conn.close()
    
    cat = random.choice(['education', 'failure', 'inspirational', 'success'])
    url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(cat)
    
    response = requests.get(url, headers={'X-Api-Key': '/2ngwp4luVWlea+ksewYXA==R0XrwKWPbcfJ37Yh'})
    
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)[0]
    else:
        data = {'quote':'', 'author':''}

    return data

def get_profile(request):
    if request.method == 'GET': 
        return render_template('users/profile.html')

    id = request.form['id']
    username = request.form['username']
    email = request.form['email']
    fullname = request.form['fullname']

    user_by_username = users_md.Users.query.filter(id!=id).filter(username==username).first()
    user_by_email = users_md.Users.query.filter(id!=id).filter(email==email).first()

    if user_by_username or user_by_email:
        flash('username or email already exist')
        return redirect('/users/profile/edit')

    user = users_md.Users.query.filter_by(id=id).first()
    user.username = username
    user.email = email
    user.fullname = fullname
    user.save()

    flash('succesfully edit your profile')
    return redirect('/users/profile')

def get_password(request):
    if request.method == 'GET': 
        return render_template('users/password.html')
    
    old = request.form['old-password']
    new = request.form['new-password']
    
    if users_md.bc.check_password_hash(current_user.password, old):
        hash = users_md.bc.generate_password_hash(new)
        user = users_md.Users.query.filter_by(id=current_user.id).first()
        user.password = hash
        user.save()

        flash('succesfully change your password')
        return redirect('/users/password')
    
    else:
        flash('your supplied wrong password')
        return render_template('users/password.html')