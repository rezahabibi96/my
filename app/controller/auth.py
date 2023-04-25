from forms import auth as auth_fr
from models import users as users_md, students as students_md
from flask import redirect, render_template, url_for
from flask_login import logout_user, login_user, current_user, login_required


def signout():
    logout_user()
    return redirect(url_for('index'))

def signup(request):
    form = auth_fr.RegisterForm(request.form)

    msg = None
    success = False

    if request.method == 'GET': 
        return render_template('auth/signup.html', form=form, msg=msg)

    if form.validate_on_submit():
        id = request.form.get('id', '', type=int)
        fullname = request.form.get('fullname', '', type=str)
        username = request.form.get('username', '', type=str)
        email = request.form.get('email', '', type=str)
        password = request.form.get('password', '', type=str)  

        user = users_md.Users.query.filter_by(id=id).first()

        user_by_username = users_md.Users.query.filter_by(username=username).first()
        user_by_email = users_md.Users.query.filter_by(email=email).first()

        if user or user_by_username or user_by_email:
            msg = 'User provided already exists'
        
        else:         
            pw = users_md.bc.generate_password_hash(password)
            
            user = users_md.Users(id, fullname, username, email, pw)
            user.save()

            student = students_md.Students(id_student=id)
            student.save()

            msg = 'User created, <a href="' + url_for('auth.signin') + '">Click here</a>!'
            success = True

    else:
        success = 'something wrong'     

    return render_template('auth/signup.html', form=form, msg=msg, success=success)

def signin(request):
    form = auth_fr.LoginForm(request.form)

    msg = None

    if form.validate_on_submit():
        id = request.form.get('id', '', type=int)
        password = request.form.get('password', '', type=str) 

        user = users_md.Users.query.filter_by(id=id).first()

        if user:        
            if users_md.bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Try again."
        else:
            msg = "unknown user"

    return render_template('auth/signin.html', form=form, msg=msg)