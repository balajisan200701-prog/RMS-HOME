from flask import render_template, request
from app.source.admin.menu.model import MenuItem as Menu


def register_routes(app):

    @app.route('/')
    def home():
        return render_template('dashboard.html')


    @app.route('/menu')
    def menu():
        category = request.args.get('category')

        daily_items = Menu.query.filter_by(status="available").all()

        if category:
            menu_items = Menu.query.filter_by(category=category).all()
        else:
            menu_items = Menu.query.all()


        return render_template('menu.html', menu=menu_items, daily_items=daily_items)