#app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , EmailField , BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo , ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    """From for new users to register"""
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    email = EmailField("Email" , validators=[DataRequired()])
    name = StringField("Name" , validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")