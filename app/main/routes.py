# app/main/routes.py
from flask import render_template, flash , request
from flask_login import login_required , current_user
from app.main import main
from app.services.jikan_service import JikanService


@main.route('/')
def index():
    """Home page with search functionality"""
    search_query = request.args.get('q', '').strip() #Get search query from URL parameters
    search_results= []
    if search_query:   #if user searched for something.
        search_results = JikanService.search_anime(search_query)
        if not search_results:
            flash(f'No results found for "{search_query}"', 'info')
    return render_template('index.html',
                           search_query=search_query,
                           search_results=search_results)

@main.route('/watchlist')
@login_required
def watchlist():
    """User's watchlist page"""
    return render_template ('main/watchlist.html')