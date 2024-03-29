from flask import Flask
import pandas as pd

# create a Flask app
app = Flask(__name__)

# read the CSV file
df_top_movies = pd.read_csv('top_movies.csv')

# make a dataframe with required columns
df = df_top_movies[['cover url', 'title', 'movieId', 'imdbId', 'tmdbId', 'rating', 'count']]

# convert dataframe to list of dicts
movies = df.to_dict('records')
 
# URL for the MovieLens website
movies_lens_url = 'https://movielens.org/movies/'

# rename columns
for movie in movies:
    movie['url'] = movie.pop('cover url')
    movie['caption'] = movie.pop('title')

@app.route("/")
def index():
    image_data = movies
    images_html = ""
    for data in image_data:
        # get the movie id and rating from the data
        movie_id = data["movieId"]
        rating = data["rating"]

        # create a link to the MovieLens site using the movie ID
        movie_link = movies_lens_url + str(movie_id)

        # add the rating and link to the image HTML
        html = movies_lens_url + str(movie_id) # add the rating and link to the image html
        images_html += f"""
        <div class='card'>
            <img src='{data["url"]}' class='card-img'>
            <div class='card-content'>
                <h3 class='card-title'>{data["caption"]}</h3>
                <p class='card-rating'>Rating: {rating}</p>
                <a href='{movie_link}' class='card-link' target='_blank'>More details</a>
            </div>
        </div>
        """

    # construct the HTML page
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MoviesLens</title>
        <style>
            * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: #000;
            color: #fff;
            font-family: 'Orbitron', sans-serif;
        }}

        h1 {{
            text-align: center;
            margin-top: 20px;
            margin-bottom: 40px;
            font-size: 36px;
            font-weight: bold;
            color: #00FFFF;
            animation: glow 2s infinite;
        }}

        @keyframes glow {{
            0% {{ text-shadow: 0 0 10px #00FFFF; }}
            50% {{ text-shadow: 0 0 20px #00FFFF; }}
            100% {{ text-shadow: 0 0 10px #00FFFF; }}
        }}

        .container {{
            max-width: 1500px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            grid-gap: 20px;
        }}

        .card {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #111;
            border-radius: 10px;
            box-shadow: inset 0 -3em 3em rgba(0,0,0,0.1), 
                        0.3em 0.3em 1em rgba(255,255,255,0.3);
            overflow: hidden;
        }}

        .card-img {{
            width: 200px;
            height: 300px;
            object-fit: cover;
            transition: transform .5s ease-in-out;
        }}   

        .card-img:hover {{
            transform: scale(1.1);
        }}

        .card-content {{
            padding: 20px;
            width: 100%;
        }}

        .card-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #00FFFF;
        }}

        .card-rating {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #8cf97b;
        }}

        .card-link {{
            display: inline-block;
            font-size: 18px;
            color: #fff;
            background-color:#00FFFF ;
            padding: 10px 20px;
            border-radius: 5px;
                text-decoration:none ;
                transition: background-color 0.3s ease; 
            }}
            .card-link:hover {{
            background-color:#8cf97b ;
            }}
            
        </style>
    </head>
    <body>
        <h1>MovieLens Top Movies</h1>
        <div class="container">
        {images_html}
        </div>
    </body>
    </html>
    """
    return html

# run the app

if __name__ == "__main__":
    app.run(debug=True)
