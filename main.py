from flask import Flask, render_template, request
import csv
from difflib import SequenceMatcher


# create a Flask app
# app = Flask(__name__)
# create a Flask app with a custom template folder
app = Flask(__name__, template_folder="my_templates")

# load the configuration from a file or environment variable
app.config.from_pyfile('config.py')


# read the CSV file
with open('top_movies.csv') as f:
    reader = csv.DictReader(f)
    # make a list of dicts with required columns
    movies = [{'url': row['cover url'], 'caption': row['title'], 'movieId': row['movieId'], 'rating': row['rating']} for row in reader]

def string_similarity(str1, str2):
    """Function to calculate the similarity between two strings

    Parameters
    ----------
    str1 : str
        First string
    str2 : str
        Second string

    Returns
    -------
    float
        Similarity between the two strings as a percentage
    """
    # create a SequenceMatcher object with the two strings
    matcher = SequenceMatcher(None, str1, str2)
    # get the similarity ratio
    ratio = matcher.ratio()
    # convert ratio to percentage and return it
    percentage = round(ratio * 100, 2) # round to two decimal places
    return percentage

def get_similar_movies(movieId):
    """Function to get a list of movies similar to the given movie

    Parameters
    ----------
    movieId : str
        The movieId of the movie for which we want to find similar movies

    Returns
    -------
    list
        A list of movies similar to the given movie
    """
    # get the movie object for the given movieId
    movie = [movie for movie in movies if movie["movieId"] == movieId][0]
    # get the title of the given movie
    title = movie["caption"]
    # create an empty list for storing similar movies
    similar_movies = []
    # loop through all the movies
    for movie in movies:
        # get the similarity ratio between the given movie and the current movie
        similarity = string_similarity(title, movie["caption"])
        # if similarity is greater than 60 and not the same movie
        if similarity > 60 and title != movie["caption"]:
            # add the current movie to the list of similar movies
            similar_movies.append(movie)
    # return the list of similar movies
    return similar_movies


@app.route("/search")
def search():
 # get the user query from the URL parameters
 query = request.args.get("query")
 # filter the movies list by matching the query with the title
 results = [movie for movie in movies if query.lower() in movie["caption"].lower()]
 # return the results to the template
 return render_template("search.html", results=results, query=query, app=app)

@app.route("/")
def index():
    # pass the movies list to the template
    return render_template('index.html', movies=movies, app=app)

# # check if index.html exists and where it is located
# import os
# print(os.path.isfile("index.html"))
# print(os.path.abspath("index.html"))


# run the app
if __name__ == "__main__":
    app.run(debug=True)
