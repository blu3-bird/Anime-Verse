# app/main/routes.py
from flask import render_template, flash , request, redirect, url_for
from flask_login import login_required , current_user
from app.main import main
from app.services.jikan_service import JikanService


@main.route('/')
def index():
    """Home page with search functionality"""
    search_query = request.args.get('q', '').strip() 
    page = request.args.get('page', 1, type=int)

    search_data = {'results': [], 'has_next_page': False}
    #Get search query from URL parameters

    # if user searched for something.
    if search_query:   
        search_data = JikanService.search_anime(search_query, page=page)

        #Show message if not results found
        if not search_data['results']:
            flash(f'No results found for "{search_query}"', 'info')

    return render_template('index.html',
                           search_query=search_query,
                           search_results=search_data['results'],
                           has_next_page=search_data['has_next_page'],
                           current_page=page)

@main.route('/watchlist')
@login_required
def watchlist():
    """User's watchlist page"""
    return render_template ('main/watchlist.html')


@main.route('/anime/<int:anime_id>')
def anime_details(anime_id):
    """Display detailed info bout a specific anime"""

    from_search = request.args.get('from_search' , "")
    page = request.args.get('page', 1, type=int)
    #to get the searched keyword.

    anime = JikanService.get_anime_details(anime_id)

    #if anime not found, show error
    if not anime:
        flash(f'Anime with {from_search} not found', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('main/anime_details.html', 
                           anime=anime,
                           from_search=from_search,
                           search_page=page)