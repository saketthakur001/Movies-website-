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
        <div style='display:inline-block; margin: 20px; text-align:center; border: 5px solid #FF0080; padding: 10px; border-radius: 10px; background-color: #333;'>
            <img src='{data["url"]}' style='max-width: 125px; max-height:300px; width:auto; height:auto;'>
            <p class='caption'>{data["caption"]}</p> <p class='rating'>Rating: {rating}</p>
            <a href='{movie_link}' class='link'>More details</a>
        </div> 
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Gallery</title>
        <style>
            body {{
                background-color: #444;
                color: #eee;
                margin: 0;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 20px;
                border-bottom: 5px solid #FF0080;
                padding-bottom: 10px;
            }}
            img {{
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background-color: #fff;
                transition: box-shadow 0.3s ease;
            }}
            img:hover {{
                box-shadow: 0 0 10px #8cf97b;
            }}
            .caption {{
                font-size: 14px;
                color: #eee;
                margin: 10px 0;
                max-width: 125px;
                word-wrap: break-word;
            }}
            .rating {{
                font-size: 12px;
                color: #eee;
                margin-bottom: 5px;
            }}
            .link {{
                font-size: 12px;
                color: #8cf97b;
                text-decoration: none;
            }}
            .link:hover {{
                text-decoration: underline;
            }}
            .accent-pink {{
                color: #FF0080;
                border-bottom: 2px solid #FF0080;
                padding-bottom: 5px;
            }}
            .accent-lime {{
                color: #8cf97b;
            }}
            
        </style>
    </head>
    <body>
        <h1>Image Gallery</h1>
        {images_html}
        <p class="accent-pink">Pink accent color</p>
        <p class="accent-lime">Lime accent color</p>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True)
# @app.route("/")
# def index():
#     image_data = movies
#     images_html = "" 
#     for data in image_data: # get the movie id and rating from the data 
#         movie_id = data["movieId"]
#         rating = data["rating"] # create a link to the movieslens site using the movie id 
#         movie_link = moveis_lens_url + str(movie_id) # add the rating and link to the image 
#         html  = moveis_lens_url + str(movie_id) # add the rating and link to the image html 
#         images_html += f""" <div style='display:inline-block; margin: 20px; text-align:center; border: 5px solid #FF0080; padding: 10px; border-radius: 10px; background-color: #333;'> <img src='{data["url"]}' style='max-width: 125px; max-height:300px; width:auto; height:auto;'> <p class='caption'>{data["caption"]}</p> <p class='rating'>Rating: {rating}</p> <a href='{movie_link}' class='link'>More details</a> </div> """
# import pandas as pd

# df = pd.read_csv('top_movies.csv')
# df.head()


# import pandas as pd
# # read the csv file
# df = pd.read_csv('top_movies.csv')

# # make a df get all the title and cover url
# df = df[['cover url', 'title']]

# # make a list of dicts
# movies = df.to_dict('records')

# # rename the title to caption and cover url to url
# for movie in movies:
#     movie['url'] = movie.pop('cover url')
#     movie['caption'] = movie.pop('title')
# movies

# # reposition the each dict 
# # get link of an image
# img = "https://m.media-amazon.com/images/M/MV5BMzMyYjg0MGMtMTlkMy00OGFiLWFiNTYtYmFmZWNmMDFlMzkwXkEyXkFqcGdeQXVyNjAwNDUxODI@.jpg"
# # what is the sapect ratio of the image
# aspect_ratio = 1.5
