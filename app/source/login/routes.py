
from flask import session, redirect, render_template, request
from app import db
from app.source.admin.worker.model import Worker
from app.source.login.model import Admin


def login_routes(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():

        # Create default admin account if it does not exist
        with app.app_context():
            db.create_all()

            admin_user = Admin.query.filter_by(
                username='admin'
            ).first()

            if not admin_user:
                admin_user = Admin(
                    username='admin',
                    password='admin123'
                )
                db.session.add(admin_user)
                db.session.commit()

        if request.method == 'POST':

            username = request.form['username']
            password = request.form['password']

            # Admin Login
            admin = Admin.query.filter_by(
                username=username,
                password=password
            ).first()

            if admin:
                session['logged_in'] = True
                session['role'] = 'admin'
                session['admin_id'] = admin.id
                return redirect('/admin')

            # Worker Login
            worker = Worker.query.filter_by(
                username=username,
                password=password,
                status='active'
            ).first()

            if worker:
                session['logged_in'] = True
                session['role'] = 'worker'
                session['worker_id'] = worker.id
                session['worker_name'] = worker.name
                return redirect('/admin/add-bill')

        return render_template('login.html')


