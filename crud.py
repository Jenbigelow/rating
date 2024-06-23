"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def all_users():
    """Returns all the movies"""

    list_of_users=User.query.all()

    return list_of_users

def get_user_by_id(user_id):
    """Get movie by ID"""
    selected_user = User.query.get(user_id)
    return selected_user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    
    return movie 

def all_movies():
    """Returns all the movies"""

    list_of_movies=Movie.query.all()

    return list_of_movies

def get_movie_by_id(movie_id):
    """Get movie by ID"""
    selected_movie = Movie.query.get(movie_id)
    return selected_movie


def mov_rating(user, movie, score): 

    rating = Rating(user=user, movie=movie, score=score)

    return rating 

def look_up_movie_rating(user_id):

    rated_movies=Rating.query.filter(Rating.user_id == user_id).all()
    return rated_movies

def look_up_movie_rating_by_movie_id(movie_id):

    rated_movies=Rating.query.filter(Rating.movie_id == movie_id).all()
    return rated_movies

def get_user_by_email(email):

    return User.query.filter(User.email == email).first()






if __name__ == '__main__':
    from server import app
    connect_to_db(app)