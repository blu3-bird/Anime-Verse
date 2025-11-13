#app/auth/routes.py
from flask import flash , request , redirect , url_for , render_template , jsonify
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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, name = form.name.data)

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Congratulations, You are now registered" ,"success")

        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title = 'Register' , form = form)

@auth.route('/login' , methods=["GET", "POST"])
def login():
    """For Registrated Users"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username = form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash ("Invalid Username or Password", 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)

        user.last_seen = datetime.utcnow()
        db.session.commit()

        flash(f'Welcome Back!, {current_user.username}!', 'success')

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
            
        return redirect(next_page)
    return render_template('auth/login.html', title ='login' , form=form )

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
    """User Profile page with Stats"""

    watchlist_items = current_user.watchlist_items.all()

    total_anime = len(watchlist_items)

    total_episodes = sum(item.episodes_watched or 0 for item in watchlist_items)

    completed_anime = sum(1 for item in watchlist_items if item.status == 'completed')

    user_ratings = current_user.ratings.all()

    avg_rating = 0
    if user_ratings:
        avg_rating = sum(r.score for r in user_ratings) / len(user_ratings)

    
    # prepare avatar data
    initials = ''
    if current_user.name:
        name_parts = current_user.name.split()

        if len(name_parts) >= 2:
            initials = name_parts[0][0] + name_parts[1][0]
        else:
            initials = name_parts[0][0:2]
        
    initials = initials.upper()

    return render_template('auth/profile.html', 
                           title = 'Profile', 
                           user = current_user,
                           total_anime = total_anime,
                           total_episodes=total_episodes,
                           completed_anime=completed_anime,
                           avg_rating= avg_rating,
                           initials=initials)

@auth.route('/update-theme', methods=['POST'])
@login_required
def update_theme():
    """Update user's theme preference"""
    
    # Get JSON data from request
    data = request.get_json()
    
    # Extract theme value
    theme = data.get('theme')
    
    # Validate theme value
    if theme not in ['dark', 'light']:
        return jsonify({'success': False, 'error': 'Invalid theme'}), 400
    
    # Update user's theme preference
    current_user.theme_preference = theme
    
    # Save to database
    try:
        db.session.commit()
        return jsonify({'success': True, 'theme': theme}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Database error'}), 500
    
@auth.route('/update-avatar',methods=['POST'])
@login_required
def update_avatar():
    """Update user Avatar"""

    data = request.get_json()

    avatar = data.get('avatar')

    # validation
    valid_avatars = [
        'initials', 'avatar_1', 'avatar_2', 'avatar_3', 'avatar_4', 'avatar_5', 'avatar_6', 'avatar_7', 'avatar_8', 'avatar_9', 'avatar_10', 'avatar_11', 'avatar_12'
    ]

    if avatar not in valid_avatars:
        return jsonify({'success':False, 'error': 'Invalid Avatar'}), 400

    current_user.avatar = avatar

    try:
        db.session.commit()
        return jsonify({'success':True, 'avatar':avatar}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success':False, 'error': 'Database Error'}), 500
    
@auth.route('/update-bio', methods=['POST'])
@login_required
def update_bio():
    bio = request.form.get('bio')

    current_user.bio = bio

    try:
        db.session.commit()
        flash('Bio Updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Unable to update to bio, try again', 'error')

    return redirect(url_for('auth.profile'))