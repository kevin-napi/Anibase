from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Anime(db.Model):
    mal_id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    score = db.Column(db.Float, nullable = False)
    synopsis = db.Column(db.String(255), nullable = False) # New
    url = db.Column(db.String(255), nullable = False)
    img_url = db.Column(db.String(255), nullable = False)
    
    def __repr__(self) -> str:
        return f"Anime: {self.id}"