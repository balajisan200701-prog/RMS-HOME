from flask import Blueprint, render_template, request, redirect, session
from app.source.admin.worker.model import Worker
from app import db
from app.source.login.auth import login_required, admin_required



def worker_routes(app):


    @app.route('/admin/worker')
    @login_required
    @admin_required
    def worker():

      

        workers = Worker.query.all()
        return render_template('worker.html', workers=workers)


    @app.route('/admin/add-worker', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def add_worker():

        if request.method == 'POST':

            name = request.form['name']
            phone = request.form['phone']
            address = request.form['address']
            status = request.form['status']
            username = request.form['username']
            password = request.form['password']

            new_worker = Worker(
                name=name,
                phone=phone,
                address=address,
                status=status,
                username=username,
                password=password
            )

            db.session.add(new_worker)
            db.session.commit()

            return redirect('/admin/worker')

        return render_template('add_worker.html')


    @app.route('/admin/delete-worker/<int:id>')
    @login_required
    @admin_required
    def delete_worker(id):

        worker = Worker.query.get(id)

        db.session.delete(worker)
        db.session.commit()

        return redirect('/admin/worker')


    @app.route('/admin/update-worker/<int:id>', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def update_worker(id):

        worker = Worker.query.get(id)

        if request.method == 'POST':

            worker.name = request.form['name']
            worker.phone = request.form['phone']
            worker.address = request.form['address']
            worker.status = request.form['status']
            worker.username = request.form['username']
            worker.password = request.form['password']

            db.session.commit()

            return redirect('/admin/worker')

        return render_template('update_worker.html', worker=worker)