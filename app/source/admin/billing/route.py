from flask import render_template, request, redirect, Response
from app import db
from app.source.admin.billing.model import BillingRecord, BillingItem
from app.source.admin.menu.model import MenuItem
from app.source.login.auth import login_required
from sqlalchemy import or_


from sqlalchemy.orm import joinedload

from flask import jsonify



from datetime import datetime
import csv
from io import StringIO


def bill_routes(app):

    # =========================
    # BILL LIST (SEARCH + DATE + PAGINATION)
    # =========================
    @app.route('/admin/bill')
    @login_required
    def billing():

        search = request.args.get('search', '')
        date_range = request.args.get('date_range', '')
        page = request.args.get('page', 1, type=int)

        per_page = 5

       
        query = BillingRecord.query.options(
            joinedload(BillingRecord.bill_items)
        )



        # SEARCH (name + phone)
        if search:
            query = query.filter(
                or_(
                    BillingRecord.customer_name.ilike(f'%{search}%'),
                    BillingRecord.phone_no.ilike(f'%{search}%')
                )
            )

        # DATE RANGE
        if date_range:
            try:
                if " to " in date_range:
                    dates = date_range.split(" to ")
                elif " - " in date_range:
                    dates = date_range.split(" - ")
                else:
                    dates = []

                if len(dates) == 2:
                    from_date = datetime.strptime(dates[0].strip(), '%d-%m-%Y')
                    to_date = datetime.strptime(dates[1].strip(), '%d-%m-%Y')
                    to_date = to_date.replace(hour=23, minute=59, second=59)
                    query = query.filter(
                        BillingRecord.date.between(from_date, to_date)
                    )

            except Exception as e:
                print("DATE ERROR:", e)

        # PAGINATION
        pagination = query.order_by(
            BillingRecord.id.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # No results flag
        not_found = search != '' and len(pagination.items) == 0

        return render_template(
            "/billing.html",
            records=pagination.items,
            pagination=pagination,
            search=search,
            not_found=not_found
        )

    # =========================
    # ADD BILL
    # =========================
    @app.route('/admin/add-bill', methods=['GET', 'POST'])
    @login_required
    def add_record():

        if request.method == "POST":

            customer_name = request.form["customer_name"]
            phone_no = request.form["phone_no"]

            item_names = request.form.getlist("item_name")
            prices = request.form.getlist("price")
            quantities = request.form.getlist("quantity")
            payment_method = request.form.get("payment_method")

            payment_status = request.form.get("payment_status")

            total_amount = float(request.form["total_amount"])
            total_qty = sum(int(q) for q in quantities)

            bill = BillingRecord(
                customer_name=customer_name,
                phone_no=phone_no,
                quantity=total_qty,
                total_amount=total_amount,
                payment_method=payment_method,
                payment_status=payment_status
            )

            db.session.add(bill)
            db.session.commit()

            for name, price, qty in zip(item_names, prices, quantities):
                db.session.add(BillingItem(
                    bill_id=bill.id,
                    item_name=name,
                    quantity=int(qty),
                    price=float(price),
                    total=float(price) * int(qty)
                ))

            db.session.commit()

            return redirect(f"/admin/print-bill/{bill.id}")

        return render_template(
            "add_bill.html",
            menu_items=MenuItem.query.all()
        )

    # =========================
    # UPDATE BILL
    # =========================
    @app.route('/admin/update-bill/<int:id>', methods=['GET', 'POST'])
    @login_required
    def update_record(id):

        record = BillingRecord.query.get_or_404(id)

        if request.method == 'POST':

            record.customer_name = request.form['customer_name']
            record.phone_no = request.form['phone_no']

            item_names = request.form.getlist("item_name")
            prices = request.form.getlist("price")
            quantities = request.form.getlist("quantity")

            BillingItem.query.filter_by(bill_id=id).delete()

            total_qty = 0
            total_amt = 0

            for name, price, qty in zip(item_names, prices, quantities):

                qty = int(qty)
                price = float(price)
                total = qty * price

                total_qty += qty
                total_amt += total

                db.session.add(BillingItem(
                    bill_id=id,
                    item_name=name,
                    quantity=qty,
                    price=price,
                    total=total
                ))

            record.quantity = total_qty
            record.total_amount = total_amt

            db.session.commit()

            return redirect('/admin/bill')

        return render_template(
            "update_bill.html",
            record=record,
            bill_items=BillingItem.query.filter_by(bill_id=id).all(),
            menu_items=MenuItem.query.all()
        )

    # =========================
    # DELETE BILL
    # =========================
    @app.route('/admin/delete-bill/<int:id>')
    @login_required
    def delete_record(id):

        BillingItem.query.filter_by(bill_id=id).delete()

        record = BillingRecord.query.get_or_404(id)

        db.session.delete(record)
        db.session.commit()

        return redirect('/admin/bill')

    # =========================
    # PRINT BILL
    # =========================
    @app.route("/admin/print-bill/<int:id>")
    @login_required
    def print_bill(id):

        record = BillingRecord.query.get_or_404(id)
        bill_items = BillingItem.query.filter_by(bill_id=id).all()

        return render_template(
            "print_bill.html",
            record=record,
            bill_items=bill_items
        )

    # =========================
    # EXPORT CSV
    # =========================
    @app.route('/admin/bill-export')
    @login_required
    def export_csv():
 
        records = BillingRecord.query.order_by(BillingRecord.id.asc()).all()
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
             'Customer Name', 'Phone',
            'Quantity', 'Total Amount', 'Date' ,'payment_method', 'payment_status'
        ])

        for r in records:
            writer.writerow([
                
                r.customer_name,
                r.phone_no,
                r.quantity,
                r.total_amount,
                r.date,
                r.payment_method,
                r.payment_status
            ])

        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=billing_records.csv'
            }
        )
      
     
# =========================
# UPDATE PAYMENT
# =========================
    @app.route('/admin/update-payment/<int:id>/<method>')
    @login_required
    def update_payment(id, method):

        record = BillingRecord.query.get_or_404(id)

        record.payment_method = method
        record.payment_status = "Paid"

        db.session.commit()

        return jsonify({
            "success": True
        })

    
