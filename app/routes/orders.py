from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import db, Table, Employee, Order, OrderDetail, MenuItem, MenuItemType
from app.forms import TableAssignmentForm, MenuItemAssignmentForm, CloseTableForm

bp = Blueprint("orders", __name__, url_prefix="")


# @bp.route("/")
# @login_required
# def index():
#     return render_template("orders.html")

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Forms for different actions
    table_form = TableAssignmentForm()
    menu_item_form = MenuItemAssignmentForm()
    close_table_form = CloseTableForm()

    # Assign Table form setup
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished == False).all()
    busy_table_ids = [order.table_id for order in open_orders]
    open_tables = [table for table in tables if table.id not in busy_table_ids]
    table_form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    table_form.servers.choices = [(e.id, e.name) for e in Employee.query.order_by(Employee.name).all()]

    # Querying current user's open orders
    user_orders = Order.query.filter_by(employee_id=current_user.id, finished=False).all()

    # Menu items query (join to MenuItemType)
    menu_items = MenuItem.query.join(MenuItemType).order_by(MenuItemType.name, MenuItem.name).all()
    menu_item_form.menu_item_ids.choices = [(item.id, item.name) for item in menu_items]

    if table_form.validate_on_submit() and table_form.assign.data:
        # Assign Table action
        new_order = Order(employee_id=table_form.servers.data, table_id=table_form.tables.data, finished=False)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for("orders.index"))

    return render_template("orders.html", 
                            table_form=table_form,
                            menu_item_form=menu_item_form,
                            close_table_form=close_table_form,
                            user_orders=user_orders,
                            menu_items=menu_items)
    
    
@bp.route("/close/<int:order_id>", methods=["POST"])
@login_required
def close_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.finished = True
    db.session.commit()
    return redirect(url_for("orders.index"))

@bp.route("/add_to_order/<int:order_id>", methods=["POST"])
@login_required
def add_to_order(order_id):
    form = MenuItemAssignmentForm()
    
    # Set the choices for the menu items before form validation
    form.menu_item_ids.choices = [(item.id, item.name) for item in MenuItem.query.all()]
    
    if form.validate_on_submit():
        for item_id in form.menu_item_ids.data:
            order_detail = OrderDetail(order_id=order_id, menu_item_id=item_id)
            db.session.add(order_detail)
        db.session.commit()
    return redirect(url_for("orders.index"))