#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from datetime import date
import json
import sys
from wsgiref.validate import validator
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model): #COMPLETED
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(550))
    shows = db.relationship('Show', backref='venue', lazy=True)

class Artist(db.Model): #COMPLETED
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(550))
    shows = db.relationship('Show', backref='artist', lazy=True)

class Show(db.Model): #COMPLETED
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable = False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable = False)
  start_time = db.Column(db.DateTime, nullable=False)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'): #DONE
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues') #COMPLETED
def venues():
  # fetch real venues data.
  data = []
  all_venues = Venue.query.all()
  unique_venues = Venue.query.distinct(Venue.city, Venue.state).all()

  # data model to be returned
  for un_venue in unique_venues:
    data.append({
      'city': un_venue.city,
      'state': un_venue.state,
      'venues':[]
    })
  # populate venues data
  for venue in all_venues:
    #calculate for num_upcoming_shows aggregating based on number of upcoming shows per venue.
    def get_upcoming_shows():
      up_shows =[]
      for show in venue.shows:
        if show.start_time > datetime.now():
          up_shows.append(show)
      return len(up_shows)

    for un_venue in data:
      if un_venue['city'] == venue.city and un_venue['state'] == venue.state:
        un_venue['venues'].append({
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': get_upcoming_shows()
        })
 
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST']) #COMPLETED
def search_venues():
  # implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  db_search_results = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  venues = Venue.query.all()

  def count_upcoming_shows():
    up_shows =[]
    for venue in venues:
      for show in venue.shows:
        if show.start_time > datetime.now():
          up_shows.append(show)
    return len(up_shows)

  def get_search_result_data():
    data = []
    for search_result in db_search_results:
      data.append({
        'id': search_result.id,
        'name': search_result.name,
        'num_upcoming_shows': count_upcoming_shows()
      })
    return data

  response={
    'count': len(db_search_results),
    'data': get_search_result_data()
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>') #COMPLETED
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.get_or_404(venue_id)
  
  def get_upcoming_shows():
    upcoming = []
    for show in venue.shows:
      if show.start_time > datetime.now():
        upcoming.append({
          'artist_id': show.artist_id,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'start_time': str(show.start_time)
        })
    return upcoming
  
  def get_past_shows():
    past = []
    for show in venue.shows:
      if show.start_time <= datetime.now():
        past.append({
          'artist_id': show.artist_id,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'start_time': str(show.start_time)
        })
    return past
  
  def get_upcoming_count():
    return len(get_upcoming_shows())   
 
  def get_past_count():
    return len(get_past_shows())
    
  data = {
    "id" : venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "address": venue.address,
    "phone": venue.phone,
    "website_link": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows":get_past_shows(),
    "upcoming_shows": get_upcoming_shows(),
    "past_shows_count": get_past_count(),
    "upcoming_shows_count": get_upcoming_count()
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET']) #DONE
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST']) #COMPLETED
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  ven_form = VenueForm(request.form)
  try:
    venue = Venue(
      name = ven_form.name.data,
      city = ven_form.city.data,
      state = ven_form.state.data,
      phone = ven_form.phone.data,
      address = ven_form.address.data,
      genres = ven_form.genres.data,
      image_link = ven_form.image_link.data,
      facebook_link = ven_form.facebook_link.data,
      seeking_talent = ven_form.seeking_talent.data,
      website_link = ven_form.website_link.data,
      seeking_description = ven_form.seeking_description.data
    )
    db.session.add(venue)
    db.session.commit()
     # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    print('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  # TODO: modify data to be the data object returned from db insertion

    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE']) #TODO
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists') #COMPLETED
def artists():
  # real data returned from querying the database
  data = Artist.query.order_by(Artist.id.asc()).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST']) #COMPLETED
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  db_search_results = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  artists = Artist.query.all()

  def count_upcoming_shows():
    up_shows =[]
    for artist in artists:
      for show in artist.shows:
        if show.start_time > datetime.now():
          up_shows.append(show)
    return len(up_shows)

  def get_search_result_data():
    data = []
    for search_result in db_search_results:
      data.append({
        'id': search_result.id,
        'name': search_result.name,
        'num_upcoming_shows': count_upcoming_shows()
      })
    return data

  response={
    'count': len(db_search_results),
    'data': get_search_result_data()
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>') #COMPLETED
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  artist = Artist.query.get_or_404(artist_id)

  def get_upcoming_shows():
    upcoming = []
    for show in artist.shows:
      if show.start_time > datetime.now():
        upcoming.append({
          'venue_id': show.venue_id,
          'venue_name': show.venue.name,
          'venue_image_link': show.venue.image_link,
          'start_time': str(show.start_time)
        })
    return upcoming
  
  def get_past_shows():
    past = []
    for show in artist.shows:
      if show.start_time <= datetime.now():
        past.append({
          'venue_id': show.venue_id,
          'venue_name': show.venue.name,
          'venue_image_link': show.venue.image_link,
          'start_time': str(show.start_time)
        })
    return past
  
  def get_upcoming_count():
    return len(get_upcoming_shows())
    
  def get_past_count():
    return len(get_past_shows())
    
  data = {
    "id" : artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website_link": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows":get_past_shows(),
    "upcoming_shows": get_upcoming_shows(),
    "past_shows_count": get_past_count(),
    "upcoming_shows_count": get_upcoming_count()
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET']) #TODO
def edit_artist(artist_id):
  form = ArtistForm()
  artist={ }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST']) #TODO
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET']) #TODO
def edit_venue(venue_id):
  form = VenueForm()
  venue={}
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST']) #TODO
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET']) #DONE
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST']) #COMPLETED
def create_artist_submission():
  artist_form = ArtistForm(request.form)
  try:
    artist = Artist(
      name = artist_form.name.data,
      city = artist_form.city.data,
      state = artist_form.state.data,
      phone = artist_form.phone.data,
      genres = artist_form.genres.data,
      image_link = artist_form.image_link.data,
      facebook_link = artist_form.facebook_link.data,
      seeking_venue = artist_form.seeking_venue.data,
      website_link = artist_form.website_link.data,
      seeking_description = artist_form.seeking_description.data
    )
    db.session.add(artist)
    db.session.commit()
     # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows') #COMPLETED
def shows():
  # displays list of shows at /shows
  # real shows data.
  data=[]
  shows = Show.query.order_by(Show.start_time.desc()).all()
  
  for show in shows:
    show_venue = Venue.query.filter_by(id=show.venue_id).first()
    show_artist = Artist.query.filter_by(id=show.artist_id).first()
    data.append({
      'venue_id': show_venue.id,
      'venue_name': show_venue.name,
      'artist_id': show_artist.id,
      'artist_name': show_artist.name,
      'artist_image_link': show_artist.image_link,
      'start_time': str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create') #DONE
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST']) #COMPLETED
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  show_form = ShowForm(request.form)

  try:
    show = Show(
      artist_id = show_form.artist_id.data,
      venue_id = show_form.venue_id.data,
      start_time = show_form.start_time.data
    )
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except:
    db.session.rollback()
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
  
  finally:
    return render_template('pages/home.html')

@app.errorhandler(404)  #DONE
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)  #DONE
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
