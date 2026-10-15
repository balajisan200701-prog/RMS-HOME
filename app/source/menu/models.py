from app import db

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    rating = db.Column(db.Float)
    description = db.Column(db.String(200))
    is_available = db.Column(db.Boolean)