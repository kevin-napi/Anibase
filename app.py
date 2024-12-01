from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from jikan import get_current_season
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 1 Row of anime
class Anime(db.Model):
    id = db.Column(db.Integer, primary_key = True) #change to anime id provided by mal
    content = db.Column(db.String(100), nullable = True) #content = user input / change to anime name
    complete = db.Column(db.Integer, default = 0)
    created = db.Column(db.DateTime, default = datetime.now())
    #rating
    
    def __repr__(self) -> str:
        return f"Anime: {self.id}"
    

with app.app_context():
        db.create_all()
        
# Routes to webpages
@app.route("/",methods=["POST","GET"])
def index():
    # Add an anime
    if request.method == "POST":
        current_anime = request.form['content']
        new_anime = Anime(content = current_anime)
        try:
            db.session.add(new_anime)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    # See all current anime
    else:
        animes = Anime.query.order_by(Anime.id).all()
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
    

        