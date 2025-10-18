#app/models.py
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    

#WATCHLIST MODEL

class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key - links to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # From Jikan API
    anime_id = db.Column(db.Integer, nullable=False, index=True)
    anime_title = db.Column(db.String(255), nullable=False)
    anime_image = db.Column(db.String(500))

    #watchlist status
    status = db.Column(db.String(20), nullable=False, default='plan_to_watch')

    #progess tracking
    episodes_watched = db.Column(db.Integer, default=0)
    total_episodes = db.Column(db.Integer) # from Jikan API

    #Timestamps
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #Constraints
    __table_args__ = (
        db.UniqueConstraint('user_id', 'anime_id', name='unique_user_anime'),
    )

    #Relationship to User
    user = db.relationship('User', backref=db.backref('watchlist_items', lazy='dynamic'))

    def __repr__(self):
        return f'<Watchlist {self.anime_title} - {self.status}>'
    

# RATING MODEL

class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #Anime Info
    anime_id = db.Column(db.Integer, nullable=False, index=True)
    anime_title = db.Column(db.String(255), nullable=False)

    #Rating (1-10 Scale)
    score = db.Column(db.Integer, nullable=False)

    #TimeStamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #Constraints
    __table_args__ =(
        db.UniqueConstraint('user_id', 'anime_id', name='unique_user_rating'),
    )

    #Relationship
    user = db.relationship('User', backref=db.backref('ratings', lazy='dynamic'))

    def __repr__(self):
        return f'<Rating {self.anime_title}: {self.score}/10>'