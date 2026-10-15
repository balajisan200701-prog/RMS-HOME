from flask import Flask

def create_app():
    app = Flask(__name__)

    
    app.config['SECRET_KEY'] = 'mysecretkey123'
    app.config['SESSION_PERMANENT'] = False

    from app.source.menu.routes import register_routes
    register_routes(app)
   
    from app.source.admin.worker.routes import worker_routes
    worker_routes(app)
    from app.source.admin.dashboard.routes import admin_routes
    admin_routes(app)
    from app.source.admin.billing.route import bill_routes
    bill_routes(app)
    from app.source.admin.sales.routes import sales_routes
    sales_routes(app)
    from app.source.admin.menu.routes import menu_routes
    menu_routes(app)
    from app.source.login.routes import login_routes
    login_routes(app)
    from app.source.admin.profile.route import profile_routes
    profile_routes(app)






 
    return app