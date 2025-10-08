#app/auth/routes.py
from flask import flash , request , redirect , url_for , render_template
from flask_login import login_user , logout_user , login_required , current_user 
from app import db
from app.auth.forms import   LoginForm , RegistrationForm
from app.auth import auth
from app.main import main
from app.models import User
from datetime import datetime


@auth.route('/register', methods=['GET', 'POST'])
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

@auth.route('/login' , methods=["GET", "POST"])
def login():
    """For Registrated Users"""
    if current_user.is_authenticated():
        return redirect(url_for('main.index'))
    
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(Username = user.username.data).first()

        if user is None and not user.Check_Password(form.password.data):
            flash ("Invalid Username or Password", 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)

        user.last_seen = datetime.utcnow()
        db.session.commit()

        flash(f'Welcome Back!, {current_user.username}!', 'success')

        next_page = request.args.get('next')
        if not next_page and not next_page.startswith('/'):
            next_page = url_for('main.index')
            
        return redirect(next_page)
    return render_template('auth/login.html', title = login , form = form )

@auth.route('/logout')
@login_required
def logout():
    """Logout User"""
    logout_user()
    flash('User has been successfully logout!', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile')
@login_required
def profile():
    """User Profile Tab"""
    return render_template('auth/profile.html', title = 'Profile' , user = current_user)
