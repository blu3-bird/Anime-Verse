# app/main/routes.py
from flask import render_template, flash
from app.main import main


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html' ,title= 'Home')