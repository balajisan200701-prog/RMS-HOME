from app import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    phone = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    address = db.Column(
        db.String(200),
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="worker"
    )