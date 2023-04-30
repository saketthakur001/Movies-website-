from flask import Flask
import pandas as pd


# create a flask app
app = Flask(__name__)


# read the csv file
df_top_movies = pd.read_csv('top_movies.csv')

# make a df get all the title, cover url, movieId, imdbId, tmdbId, rating, count
df = df_top_movies[['cover url', 'title', 'movieId', 'imdbId', 'tmdbId', 'rating', 'count']]

# make a list of dicts
movies = df.to_dict('records')

moveis_lens_url =  'https://movielens.org/movies/' # add the movie id at the end to get the the movie page

# rename the title to caption and cover url to url
for movie in movies:
    movie['url'] = movie.pop('cover url')
    movie['caption'] = movie.pop('title')


@app.route("/")
def index():
    image_data = movies
    images_html = "" 
    for data in image_data: # get the movie id and rating from the data 
        movie_id = data["movieId"]
        rating = data["rating"] # create a link to the movieslens site using the movie id 
        movie_link = moveis_lens_url + str(movie_id) # add the rating and link to the image 
        html  = moveis_lens_url + str(movie_id) # add the rating and link to the image html 
        images_html += f""" 
        <div class='card'>
            <img src='{data["url"]}' class='card-img'>
            <div class='card-content'>
                <h3 class='card-title'>{data["caption"]}</h3>
                <p class='card-rating'>Rating: {rating}</p>
                <a href='{movie_link}' class='card-link'>More details</a>
            </div>
        </div> 
        """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Gallery</title>
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                background-color: #f0f0f0;
                color: #333;
                font-family: Roboto, sans-serif;
            }}
            h1 {{
                text-align: center;
                margin-top: 20px;
                margin-bottom: 40px;
                font-size: 36px;
                font-weight: bold;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                grid-gap: 20px;
            }}
            .card {{
                display: flex;
                flex-direction: column;
                align-items: center;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .card-img {{
                width: 100%;
                height: auto;
            }}
            .card-content {{
                padding: 20px;
                width: 100%;
            }}
            .card-title {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .card-rating {{
                font-size: 18px;
                margin-bottom: 10px;
            }}
            .card-link {{
                display: inline-block;
                font-size: 18px;
                color: #fff;
                background-color:#FF0080 ;
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
        <h1>Image Gallery</h1>
        <div class="container">
        {images_html}
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True)