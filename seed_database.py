"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

os.system("dropdb ratings")
os.system('createdb ratings')

connect_to_db(app)
app.app_context().push()
db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title = movie.get("title")
    overview = movie.get("overview")
    release_date = datetime.strptime(movie.get("release_date"), "%Y-%m-%d")
    poster_path = movie.get("poster_path")
    movies_in_db.append(crud.create_movie(title, overview, release_date, poster_path))
    
db.session.add_all(movies_in_db)
db.session.commit()
   
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'
    user_in_db = crud.create_user(email, password)
    db.session.add(user_in_db)
    for i in range(10):
        rating_number = randint(1,5)
        selected_movie = choice(movies_in_db)
        movie_rating = crud.mov_rating(user_in_db, selected_movie, rating_number)
        db.session.add(movie_rating)
db.session.commit()
    

    # TODO: create a user here

    # TODO: create 10 ratings for the user

