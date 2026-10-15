from app import db


class MenuItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    menu_id = db.Column(db.String(20), unique=True, nullable=False)         

    item_name = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(100))

    price = db.Column(db.Float, nullable=False)

    description = db.Column(db.Text)

    image = db.Column(db.String(200))

    status = db.Column(db.String(20), nullable=False)