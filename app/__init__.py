from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'mysecretkey123'
    )
    app.config['SESSION_PERMANENT'] = False

    database_url = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:balaji@localhost:5432/refdr_db'
    )

    if database_url.startswith('postgres://'):
        database_url = database_url.replace(
            'postgres://', 'postgresql://', 1
        )

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    db.init_app(app)

    with app.app_context():
    from  app.source.admin.menu.model import MenuItem
    db.create_all()

    from app.source.menu.routes import register_routes
    from app.source.admin.worker.routes import worker_routes
    from app.source.admin.dashboard.routes import admin_routes
    from app.source.admin.billing.route import bill_routes
    from app.source.admin.sales.routes import sales_routes
    from app.source.admin.menu.routes import menu_routes
    from app.source.login.routes import login_routes
    from app.source.admin.profile.route import profile_routes

    profile_routes(app)
    worker_routes(app)
    admin_routes(app)
    bill_routes(app)
    sales_routes(app)
    menu_routes(app)
    register_routes(app)
    login_routes(app)

    return app
