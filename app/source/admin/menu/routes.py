from flask import Blueprint, render_template, request, redirect, session
from app.source.admin.menu.model import MenuItem
from werkzeug.utils import secure_filename
from app import db
import os
from app.source.login.auth import login_required


UPLOAD_FOLDER = 'app/static/images/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def menu_routes(app):

    @app.route('/admin/menu')
    @login_required
    def admin_menu():

     
        search = request.args.get('search', '')
        category = request.args.get('category', '')

        query = MenuItem.query

        if search:
            query = query.filter(
                MenuItem.item_name.ilike(f'%{search}%')
            )

        if category:
            query = query.filter(
                MenuItem.category == category
            )

        page = request.args.get('page', 1, type=int)
        per_page = 5

        pagination = query.order_by(MenuItem.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return render_template(
            'menu-admin.html',
            items=pagination.items,
            pagination=pagination,
            search=search,
            category=category
        )


    @app.route('/admin/add-menu', methods=['GET', 'POST'])
    @login_required
    def add_item():
        if request.method == 'POST':
            name = request.form['item_name']

            category = request.form['category']

            price = request.form['price']

            description = request.form['description']
            image_file = request.files['image']
            status = request.form['status']

            filename = ""

            if image_file:

                filename = secure_filename(image_file.filename)

                image_path = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )

                image_file.save(image_path)

            last_item = MenuItem.query.order_by(MenuItem.id.desc()).first()

            if last_item:
              next_num = int(last_item.menu_id[1:]) + 1
            else:
               next_num = 1

            menu_id = f"I{next_num:03d}"

            new_item = MenuItem(
                menu_id=menu_id,
                item_name=name,
                category=category,
                price=price,
                description=description,
                image=filename,
                status=status
            )
           

           
            db.session.add(new_item)

            db.session.commit()

            return redirect('/admin/menu')
        return render_template('add-menu.html')


    @app.route('/admin/delete-menu/<int:id>')
    @login_required
    def delete_item(id):

        item = MenuItem.query.get(id)

        db.session.delete(item)

        db.session.commit()

        return redirect('/admin/menu')



    @app.route('/admin/update-menu/<int:id>', methods=['GET', 'POST'])
    @login_required
    def update_item(id):
        item = MenuItem.query.get(id)

        if request.method == 'POST':
            item.item_name = request.form['item_name']

            item.category = request.form['category']

            item.price = request.form['price']

            item.description = request.form['description']

            image_file = request.files['image']

            if image_file and image_file.filename:
               filename = secure_filename(image_file.filename)

               image_file.save(os.path.join(UPLOAD_FOLDER, filename))

               item.image = filename

               item.status = request.form['status']

            db.session.commit()

            return redirect('/admin/menu')

        return render_template('update-menu.html', item=item)