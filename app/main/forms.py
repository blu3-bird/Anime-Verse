from flask_wtf import FlaskForm
from wtforms import SelectField , IntegerField , SubmitField, HiddenField
from wtforms.validators import DataRequired , NumberRange, Optional

class AddToWatchlistForm(FlaskForm):
    """Form for adding anime to Watchlist"""

    #Hidden Fields (data from details page)
    anime_id = HiddenField('Anime ID', validators=[DataRequired()])
    anime_title = HiddenField('Anime Title', validators=[DataRequired()])
    anime_image = HiddenField('Anime Image')
    total_episodes = HiddenField('Total Episodes')

    #User Choice
    status = SelectField(
        'Status',
        choices=[
            ('watching', 'Watching'),
            ('completed', 'Completed'),
            ('plan_to_watch', 'Plan to Watch'),
            ('on_hold', 'On Hold'),
            ('dropped', 'Dropped')
        ],
        default='plan_to_watch',
        validators=[DataRequired()]
    )

    episodes_watched = IntegerField(
        'Episodes Watched',
        default=0,
        validators=[
            Optional(),
            NumberRange(min=0, message='Episodes cannot be negative')
        ]
    )

    submit = SubmitField('😈 Add to Watchlist')