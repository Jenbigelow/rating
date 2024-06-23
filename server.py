"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ Homepage """
    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    """View all movies"""
    movies = crud.all_movies()

    return render_template("all_movies.html", movies=movies)

@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    """See the details of a movie"""
    one_movie = crud.get_movie_by_id(movie_id)
    ratings = crud.look_up_movie_rating_by_movie_id(movie_id)
    
    return render_template("movie_details.html", movie=one_movie, ratings=ratings) 

@app.route('/users')
def users():

    all_users = crud.all_users()
    return render_template("all_users.html", users=all_users)

@app.route('/user/<user_id>')
def user_details(user_id):

    one_user = crud.get_user_by_id(user_id)
    ratings = crud.look_up_movie_rating(user_id)
    return render_template("user_details.html",user=one_user, ratings = ratings )


@app.route("/users", methods=["POST"])
def create_account():
    email = request.form.get("email")
    password = request.form.get("password")
    
    account_user = crud.get_user_by_email(email)
    if account_user == None:
        create_user = crud.create_user(email, password)
        db.session.add(create_user)
        db.session.commit()

        flash("Account creation successful!") 
    else:
        flash("User already exists!")
    return redirect('/')

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    account_user = crud.get_user_by_email(email)
    if password == account_user.password:
        primary_key = account_user.user_id
        session['primary_key'] = primary_key
        flash(f"Logged in!")

    return redirect('/')

@app.route('/ratings/<movie_id>', methods=["POST"])
def make_a_new_rating(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    score = request.form.get("score")
    # score= int(score.value())
    primary_key = session.get('primary_key')
    user = crud.get_user_by_id(primary_key)

    rating = crud.mov_rating(user = user, movie = movie, score = score)
    db.session.add(rating)
    db.session.commit()
    return redirect('/movies')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)
