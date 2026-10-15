from flask import render_template, session, redirect, request
from app import db
from app.source.admin.worker.model import Worker
from app.source.admin.menu.model import MenuItem
from app.source.admin.billing.model import BillingRecord
from app.source.login.auth import login_required, admin_required

from sqlalchemy import func
from datetime import date, datetime


def admin_routes(app):

    @app.route('/admin')
    @app.route('/admin/dashboard')
    @login_required
    @admin_required
    def admin():

        page = request.args.get('page', 1, type=int)
        per_page = 5

        # DATE RANGE
        date_range = request.args.get("date_range", "").strip()

        query = BillingRecord.query

        if date_range:
            try:
                start_str, end_str = date_range.split(" to ")

                start_date = datetime.strptime(
                    start_str.strip(),
                    "%Y-%m-%d"
                ).date()

                end_date = datetime.strptime(
                    end_str.strip(),
                    "%Y-%m-%d"
                ).date()

                query = query.filter(
                    func.date(BillingRecord.date) >= start_date,
                    func.date(BillingRecord.date) <= end_date
                )

            except:
                pass

        total_workers = Worker.query.filter_by(
            status="active"
        ).count()

        total_items = MenuItem.query.filter_by(
            status="Available"
        ).count()

        today = date.today()

        total_orders = query.count()

        total_revenue = db.session.query(
            func.sum(BillingRecord.total_amount)
        ).filter(
            BillingRecord.id.in_(
                query.with_entities(BillingRecord.id)
            )
        ).scalar() or 0

        today_customers = db.session.query(
            func.count(
                func.distinct(BillingRecord.phone_no)
            )
        ).filter(
            BillingRecord.id.in_(
                query.with_entities(BillingRecord.id)
            )
        ).scalar() or 0

        monthly_revenue = db.session.query(
            func.sum(BillingRecord.total_amount)
        ).filter(
            func.extract('month', BillingRecord.date) == today.month,
            func.extract('year', BillingRecord.date) == today.year
        ).scalar() or 0

        # PAGINATION
        pagination = query.order_by(
            BillingRecord.id.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        records = pagination.items

        # CHART DATA
        chart_data = (
            query.with_entities(
                func.date(BillingRecord.date).label("date"),
                func.sum(BillingRecord.total_amount).label("revenue"),
                func.count(BillingRecord.id).label("orders")
            )
            .group_by(func.date(BillingRecord.date))
            .order_by(func.date(BillingRecord.date))
            .all()
        )

        chart_labels = [
            str(row.date)
            for row in chart_data
        ]

        chart_revenue = [
            float(row.revenue or 0)
            for row in chart_data
        ]

        chart_orders = [
            int(row.orders or 0)
            for row in chart_data
        ]

        return render_template(
            "admin.html",

            total_workers=total_workers,
            total_items=total_items,

            total_orders=total_orders,
            total_revenue=total_revenue,
            today_customers=today_customers,
            monthly_revenue=monthly_revenue,

            records=records,
            pagination=pagination,

            chart_labels=chart_labels,
            chart_revenue=chart_revenue,
            chart_orders=chart_orders,

            date_range=date_range
        )

    @app.route('/admin/logout')
    def logout():
        session.clear()
        return redirect('/login')