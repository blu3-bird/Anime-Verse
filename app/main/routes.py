# app/main/routes.py
from flask import render_template, flash , request, redirect, url_for , jsonify
from flask_login import login_required , current_user
from app.main import main
from app.services.jikan_service import JikanService
from app import db 
from app.models import Watchlist
from app.main.forms import AddToWatchlistForm


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
    """User's watchlist page with tabs for different statuses"""

    #Get the active tab (default to 'watching')
    active_status = request.args.get('status', 'watching')

    # Valid  statuses
    valid_statuses = ['watching', 'completed','plan_to_watch', 'on_hold', 'dropped']

    # if invalid status, default to wathching
    if active_status not in valid_statuses:
        active_status = 'watching'

    # Get all watchlist items for current user.
    all_items = current_user.watchlist_items.all()

    #Organize items by status (for tabs)
    items_by_status = {
        'watching': [],
        'completed': [],
        'plan_to_watch': [],
        'on_hold': [],
        'dropped': []
    }

    for item in all_items:
        items_by_status[item.status].append(item)

    # Get the items for the active tab
    active_items = items_by_status[active_status]

    #Calculate stats
    total_anime = len(all_items)
    total_episodes = sum(item.episodes_watched or 0 for item in all_items)

    # Calculate average rating (if user has ratings)
    user_ratings = current_user.ratings.all()
    avg_rating = 0
    if user_ratings:
        avg_rating = sum(r.score for r in user_ratings) / len(user_ratings)

    # count for each status ( for tab badges)
    status_counts = {
        status: len(items_by_status[status])
        for status in valid_statuses
    }

    return render_template('main/watchlist.html',
                           active_items=active_items,
                           active_status=active_status,
                           status_counts=status_counts,
                           total_anime=total_anime,
                           total_episodes=total_episodes,
                           avg_rating=avg_rating)

@main.route('/watchlist/episode/increment/<int:item_id>', methods=['POST'])
@login_required
def increment_episodes(item_id):
    """Increment episodes count with validation"""

    # Get the watchlist item from database
    item = Watchlist.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Validation Check if already at maximum episodes
    if item.total_episodes and item.episodes_watched >= item.total_episodes:
        return jsonify({'error': 'Already at maximum episodes'}), 400
    item.episodes_watched += 1

    # Auto-complete if user just finished all episodes, mark a completed.

    auto_completed = False
    if item.total_episodes and item.episodes_watched == item.total_episodes:
        if item.status != 'completed':
            item.status = 'completed'
            auto_completed = True
        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'episodes_watched': item.episodes_watched,
                'total_episodes': item.total_episodes,
                'status': item.status,
                'auto-completed' : auto_completed
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update episode count'}), 500
        

@main.route('/watchlist/episode/decrement/<int:item_id>', methods=['POST'])
@login_required
def decrement_episode(item_id):
    """Decrement episode count with reverse auto-complete logic"""

    item = Watchlist.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if item.episodes_watched <= 0:
        return jsonify({'error': 'Already at 0 Episodes'}), 400
    item.episodes_watched -= 1

    # Reverse auto-complted
    status_changed = False
    if item.status == 'completed' and item.total_episodes:
        if item.episodes_watched < item.total_episodes:
            item.status = 'watching'
            status_changed = True

    try:
        db.sessin.commit()

        return jsonify ({
            'success': True,
            'episodes_watched': item.episodes_watched,
            'total_episodes': item.total_episodes,
            'status': item.status,
            'status_changed': status_changed
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'error': 'Failed to update episode count' }), 500
    
@main.route('/watchlist/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_watchlist(item_id):
    """Remove anime from user's watchlist"""

    item = Watchlist.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    anime_title = item.anime_title

    db.session.delete(item)

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'{anime_title} removed from the watchlist',
            'anime_title': anime_title
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove from watchlist'}), 500

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
    
    #Check if anime is in user's watchlist (if logged in)

    in_watchlist = None
    if current_user.is_authenticated:
        in_watchlist =  Watchlist.query.filter_by(
            user_id=current_user.id,
            anime_id=anime_id
        ).first()

    #create form and pre fill with anime data
    form=AddToWatchlistForm()
    form.anime_id.data = anime['mal_id']
    form.anime_title.data = anime['title']
    form.anime_image.data = anime['images']['jpg']['large_image_url']
    form.total_episodes.data = anime.get('episodes', '')
    
    return render_template('main/anime_details.html', 
                           anime=anime,
                           from_search=from_search,
                           search_page=page,
                           form=form,
                           in_watchlist=in_watchlist)


@main.route('/watchlist/add', methods=['POST'])
@login_required
def add_to_watchlist():
    """Add anime to user's Watchlist"""
    form= AddToWatchlistForm()

    if form.validate_on_submit():

        #Check if anime is already in watchlist
        existing = Watchlist.query.filter_by(
            user_id=current_user.id,
            anime_id=form.anime_id.data
        ).first()

        if existing:
            flash(f'{form.anime_title.data} is already in your watchlist!', 'warninng')
            return redirect(url_for('main.anime_details', anime_id=form.anime_id.data))
        
        # Create new Watchlist entry

        watchlist = Watchlist(
            user_id=current_user.id,
            anime_id=form.anime_id.data,
            anime_title=form.anime_title.data,
            anime_image=form.anime_image.data,
            status=form.status.data,
            total_episodes=int(form.total_episodes.data) if form.total_episodes.data else None,
            episodes_watched=form.episodes_watched.data or 0
        )

        try:
            db.session.add(watchlist)
            db.session.commit()

            flash(f'Successfully added {form.anime_title.data} to your Watchlist!', 'success')
            return redirect(url_for('main.watchlist'))
        
        except  Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            print(f'Error adding to watchlist: {e}')
            return redirect(url_for('main.anime_details', anime_id=form.anime_id.data))
        
    # If form validation failed
    flash("Please check your input and try again., 'danger'")
    return redirect(url_for('main.anime_details', anime_id=request.form.get('anime_id', 1)))
