from flask import Flask, render_template, request
import csv
from difflib import SequenceMatcher
import re
# import Levenshtein


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


def levenshtein_distance(string1, string2):
    # initialize the matrix
    m = len(string1)
    n = len(string2)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]

    # fill the matrix with the edit distances
    for i in range(m + 1):
        matrix[i][0] = i # the cost of deleting all characters from string1
    for j in range(n + 1):
        matrix[0][j] = j # the cost of inserting all characters from string2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if string1[i - 1] == string2[j - 1]:
                # if the characters match, no edit is required
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                # if the characters don't match, choose the minimum cost among insertion, deletion, or substitution
                matrix[i][j] = min(matrix[i - 1][j] + 1, # deletion
                                matrix[i][j - 1] + 1, # insertion
                                matrix[i - 1][j - 1] + 1) # substitution
    # return the edit distance
    return matrix[m][n]


def string_similarity(string1, string2):
    # preprocess the strings
    string1 = preprocess(string1)
    string2 = preprocess(string2)
    # calculate the levenshtein distance
    # distance = Levenshtein.distance(string1, string2)
    distance = levenshtein_distance(string1, string2)

    # calculate the similarity score
    similarity = 100 * (1 - distance / max(len(string1), len(string2)))
    # return the similarity score
    return similarity

def preprocess(string):
    # convert to lowercase
    string = string.lower()
    # remove punctuation and whitespace
    string = re.sub(r"\W+", "", string)
    # split into words
    words = string.split()
    # sort words alphabetically
    words.sort()
    # join words back into a string
    string = "".join(words)
    # return the preprocessed string
    return string

@app.route("/search")
def search():
    # get the user query from the URL parameters
    query = request.args.get("query")
    # create an empty list to store the results
    results = []
    # loop through the movies list
    for movie in movies:
        # check if the query is similar to the movie title
        if string_similarity(query, movie["caption"]) > 30:
            # append the movie to the results list
            results.append(movie)
    # sort the results by similarity percentage
    results = sorted(results, key=lambda x: string_similarity(query, x["caption"]), reverse=True)[:20]
    # return the results to the template
    return render_template("search.html", results=results, query=query, app=app)

@app.route("/")
def index():
    # pass the movies list to the template
    return render_template('index.html', movies=movies, app=app)

# run the app
if __name__ == "__main__":
    app.run(debug=True)
