from flask import Flask, render_template, request
import csv

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
