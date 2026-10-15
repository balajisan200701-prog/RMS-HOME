from flask import Flask, session, redirect, render_template, request
from app.source.admin.worker.model import Worker
from app.source.login.model import Admin

def login_routes(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():

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

                print("ADMIN SESSION:", session)

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
    

