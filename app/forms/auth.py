from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
	id = StringField(u'id', validators=[DataRequired()])
	password = PasswordField(u'password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
	id = StringField(u'id', validators=[DataRequired()])
	fullname = StringField(u'fullname', validators=[DataRequired()])
	username = StringField(u'username', validators=[DataRequired()])
	email = StringField(u'email', validators=[DataRequired(), Email()])
	password = PasswordField(u'password', validators=[DataRequired()])