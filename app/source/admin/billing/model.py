import re

from app import db
from datetime import datetime


class BillingRecord(db.Model):
    __tablename__ = "billing_record"

    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(15))

    quantity = db.Column(db.Integer)
    total_amount = db.Column(db.Float)

    payment_method = db.Column(db.String(50))

    payment_status = db.Column(db.String(50))

  
    date = db.Column(db.DateTime, default=datetime.utcnow)




    # 🔥 RELATIONSHIP (IMPORTANT)
    bill_items = db.relationship(
        "BillingItem",
        backref="bill",
        lazy=True,
        cascade="all, delete-orphan"
    )


class BillingItem(db.Model):
    __tablename__ = "billing_item"

    id = db.Column(db.Integer, primary_key=True)

    bill_id = db.Column(
        db.Integer,
        db.ForeignKey("billing_record.id")
    )

    item_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    total = db.Column(db.Float, nullable=False)

