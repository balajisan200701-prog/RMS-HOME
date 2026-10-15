from flask import render_template, request
from sqlalchemy import func, distinct
from datetime import datetime

from app.source.admin.billing.model import BillingRecord
from app.source.login.auth import login_required, admin_required


def sales_routes(app):

    @app.route('/admin/sales', methods=['GET'])
    @login_required
    @admin_required
    def sales_report():

        date_range = request.args.get("date_range", "").strip()
        page = request.args.get("page", 1, type=int)

        start_date = None
        end_date = None

        # DATE FILTER
        if date_range:
            try:
                start_str, end_str = date_range.split(" to ")

                start_date = datetime.strptime(
                    start_str.strip(),
                    "%d-%m-%Y"
                )

                end_date = datetime.strptime(
                    end_str.strip(),
                    "%d-%m-%Y"
                )

            except Exception as e:
                print("Date Error:", e)

        query = BillingRecord.query

        if start_date and end_date:
            query = query.filter(
                BillingRecord.date >= start_date,
                BillingRecord.date <= end_date
            )

        # SALES SUMMARY
        sales_data = (
            query.with_entities(
                func.date(BillingRecord.date).label("date"),
                func.sum(BillingRecord.total_amount).label("totalsales"),
                func.count(BillingRecord.id).label("totalorders"),
                func.avg(BillingRecord.total_amount).label("avgorderval"),
                func.count(
                    distinct(BillingRecord.customer_name)
                ).label("totalcustomer")
            )
            .group_by(func.date(BillingRecord.date))
            .order_by(func.date(BillingRecord.date))
            .all()
        )

        # CHART DATA
        chart_labels = []
        chart_values = []

        for row in sales_data:

            if hasattr(row.date, "strftime"):
                chart_labels.append(
                    row.date.strftime("%d-%m-%Y")
                )
            else:
                chart_labels.append(str(row.date))

            chart_values.append(
                float(row.totalsales or 0)
            )

        print(chart_labels)
        print(chart_values)

        # PAGINATION
        pagination = (
            query.order_by(BillingRecord.date.desc())
            .paginate(
                page=page,
                per_page=5,
                error_out=False
            )
        )

        records = pagination.items

        total_sales = sum(
            float(x.totalsales or 0)
            for x in sales_data
        )

        total_orders = sum(
            x.totalorders or 0
            for x in sales_data
        )

        total_customers = sum(
            x.totalcustomer or 0
            for x in sales_data
        )

        return render_template(
            "sales.html",

            sales=sales_data,
            records=records,

            chart_labels=chart_labels,
            chart_values=chart_values,

            total_sales=total_sales,
            total_orders=total_orders,
            total_customers=total_customers,

            date_range=date_range,
            pagination=pagination
        )