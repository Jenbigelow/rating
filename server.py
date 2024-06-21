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
    
    return render_template("movie_details.html", movie=one_movie) 

@app.route('/users')
def users():

    all_users = crud.all_users()
    return render_template("all_users.html", users=all_users)

@app.route('/user/<user_id>')
def user_details(user_id):

    one_user = crud.get_user_by_id(user_id)
    return render_template("user_details.html",user=one_user )


@app.route("/users", methods=["POST"])
def create_account():
    email = request.form.get("email")
    
    account_user = crud.get_user_by_email(email)
    if account_user == None:
        flash("Account creation successful!") 
    else:
        flash("User already exists!")
    return render_template('homepage.html', user=account_user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)
