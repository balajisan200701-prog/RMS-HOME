from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mysecretkey123'
    app.config['SESSION_PERMANENT'] = False
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:balaji@localhost:5432/rms'

    db.init_app(app)

    
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