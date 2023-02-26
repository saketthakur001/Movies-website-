from flask import Flask
import pandas as pd

app = Flask(__name__)


df = pd.read_csv('top_movies.csv')

# make a df get all the title and cover url
df = df[['cover url', 'title']]

# make a list of dicts
movies = df.to_dict('records')

# rename the title to caption and cover url to url
for movie in movies:
    movie['url'] = movie.pop('cover url')
    movie['caption'] = movie.pop('title')


@app.route("/")
def index():
    image_data = movies
    images_html = ""
    for data in image_data:
        images_html += f"""
        <div style='display:inline-block; margin: 20px; text-align:center; border: 5px solid #FF0080; padding: 10px; border-radius: 10px; background-color: #333;'>
            <img src='{data["url"]}' style='max-width:300px; max-height:300px; width:auto; height:auto;'>
            <p>{data["caption"]}</p>
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
            p {{
                font-size: 14px;
                color: #eee;
                margin: 10px 0;
                word-wrap: break-word;
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

# word-wrap: break-all; to word-wrap: break-word;