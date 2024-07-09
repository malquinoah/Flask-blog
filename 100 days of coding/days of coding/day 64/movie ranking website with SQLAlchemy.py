import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret')
Bootstrap5(app)


# CREATE DB


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-practice-sqlalchemy.db"
db.init_app(app)


# CREATE TABLE


class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# with app.app_context():
# db.create_all()

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
#
# db.session.add(new_movie)
# db.session.add(second_movie)
# db.session.commit()


class RateMovieForm(FlaskForm):
    new_rating = StringField('Your rating out of 10 (e.g., 7.5)', validators=[DataRequired()])
    new_review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')


class AddMovie(FlaskForm):
    title_field = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


API_KEY = os.getenv('api_key')
API_READ_ACCESS_TOKEN = os.getenv('api_read_access_token')


@app.route("/")
def home():
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    movie = db.get_or_404(Movie, id)
    form = RateMovieForm()
    if form.validate_on_submit():
        movie.rating = form.new_rating.data
        movie.review = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie)


@app.route('/delete/<int:id>')
def delete(id):
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = AddMovie()
    if form.validate_on_submit():
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYTdiMzI5NmNkYTU1NmE4OGQ2ZGI5MmM3YTg5MTE2NCIsInN1YiI6IjY2NDEyY2JmYmNkNDRmYzcyODRkYzJiYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rBKEVJSX2jsWm7xx4wC_svJT921Z9WEqAZF8h8Tt3yM"
        }
        params = {'query': form.title_field.data}
        movies_information = requests.get('https://api.themoviedb.org/3/search/movie', headers=headers, params=params).json()['results']
        return render_template('select.html', movies=movies_information)
    return render_template('add.html', form=form)


@app.route('/find/<int:id>')
def find(id):
    movie_id = id
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYTdiMzI5NmNkYTU1NmE4OGQ2ZGI5MmM3YTg5MTE2NCIsInN1YiI6IjY2NDEyY2JmYmNkNDRmYzcyODRkYzJiYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rBKEVJSX2jsWm7xx4wC_svJT921Z9WEqAZF8h8Tt3yM"
    }
    params = {'movie_id': movie_id}
    movie_details = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}', headers=headers, params=params).json()
    new_movie = Movie(
        title=movie_details['original_title'],
        year=movie_details['release_date'].split('-')[0],
        description=movie_details['overview'],
        img_url=f'https://image.tmdb.org/t/p/original{movie_details["poster_path"]}'
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
