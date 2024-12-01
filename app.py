from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Anime, db
from datetime import datetime
from jikan import fetch_season_animes

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app,db)

db.init_app(app)

with app.app_context():
        db.create_all()
        
def get_season_animes():
    dict_season_animes = fetch_season_animes() # Dictionary of all seasonal animes
    
    
    for anime in dict_season_animes:  # Assuming it's a list of dictionaries
        if not Anime.query.filter_by(mal_id=anime['mal_id']).first():  # Avoid duplicates
            new_anime = Anime(
                mal_id = anime['mal_id'],
                title = anime['title'],
                score = anime.get('score', 0),  # Default score to 0 if missing
                synopsis = anime['synopsis'],
                url = anime['url'],
                img_url = anime['img_url']
            )
            db.session.add(new_anime)

    db.session.commit()
    
# Routes to webpages
@app.route("/",methods=["POST","GET"])
def index():
    get_season_animes()
    animes = Anime.query.all()
    return render_template("index.html", animes=animes)
    
    
#Delete Item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_anime = Anime.query.get_or_404(id)
    try:
        db.session.delete(delete_anime)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

# Edit an anime
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id: int):
    anime = Anime.query.get_or_404(id)
    if request.method == "POST":
        anime.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template('edit.html', anime=anime)

    
if __name__ == "__main__":
    app.run(debug=True)
    

        