from flask import render_template, session
from app.source.login.auth import login_required
from flask import request, render_template, redirect, session
from app.source.login.model import Admin
from app.source.admin.worker.model import Worker
from app import db

def profile_routes(app):

    @app.route('/admin/profile')
    @login_required
    def profile():

        return render_template('profile.html')
    
    @app.route('/worker/profile')
    @login_required
    def worker_profile():

        return render_template('profile.html')   
    




    @app.route('/change-password', methods=['GET','POST'])
    @login_required
    def change_password():

        if request.method == 'POST':

            old_password = request.form['old_password']
            new_password = request.form['new_password']

            # Admin
            if session['role'] == 'admin':

                admin = Admin.query.get(session['admin_id'])

                if admin.password == old_password:

                    admin.password = new_password

                    db.session.commit()

                    return redirect('/admin/profile')

            # Worker
            if session['role'] == 'worker':

                worker = Worker.query.get(
                    session['worker_id']
                )

                if worker.password == old_password:

                    worker.password = new_password

                    db.session.commit()

                    return redirect('/admin/profile')

        return render_template('change_password.html')