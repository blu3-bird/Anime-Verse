#app/auth/routes.py
from flask import flash , request , redirect , url_for , render_template
from flask_login import login_user , logout_user , login_required , current_user 
from app import db
from app.auth.forms import   LoginForm , RegistrationForm
from app.auth import auth
from app.main import main
from app.models import User
from datetime import datetime


@auth.route('/register', Methods=['GET', 'POST'])
def register():
    """Register a new User"""
    if current_user.is_authenticated():
        return redirect(url_for(main.index))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(Username = form.username.data, email = form.email.data)

        user = User.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Congratulations, You are now registered" "success")

        return redirect(url_for(auth.login))
    
    return render_template('auth/register.html', title = 'Register' , form = form)