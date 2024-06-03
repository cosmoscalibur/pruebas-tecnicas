from pathlib import Path
import datetime
import json
from flask import Flask, request, jsonify, url_for, render_template, redirect
from flasgger import swag_from

try:
    import beitech_app
    import beitech_app.database as dbman
    from beitech_app.forms import OrdersForm, CreateForm
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).absolute().parent.parent))
    import beitech_app
    import beitech_app.database as dbman
    from beitech_app.forms import OrdersForm, CreateForm

with open(
    Path(beitech_app.__file__).parent.joinpath("settings.json"), "r"
) as json_file:
    settings = json.load(json_file)["service"]
app = Flask(__name__)
app.config["SECRET_KEY"] = settings["SECRET_KEY"]
app.config["WTF_CSRF_SECRET_KEY"] = settings["WTF_CSRF_SECRET_KEY"]


@app.route("/")
@app.route("/home")
def home():
    return render_template(
        "layout.html",
        template="form-template",
        customer_orders=customer_orders,
    )


@app.route("/customer_orders", methods=["GET", "POST"])
@swag_from("swagger/customer_orders.yml", methods=['GET'])
def customer_orders():
    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        bdate = request.form["bdate"]
        edate = request.form["edate"]
        customer_orders = dbman.get_customer_orders(customer_id, bdate, edate)
        return render_template(
            "customer_orders.html",
            template="form-template",
            customer_orders=customer_orders,
        )
    else:
        customer_id = int(request.args.get("customer_id"))
        bdate = request.args.get("bdate")
        edate = request.args.get("edate")
        return jsonify(dbman.get_customer_orders(customer_id, bdate, edate))


@app.route("/form_list_orders")
def form_list_orders():
    """Standard `contact` form."""
    form = OrdersForm()
    return render_template("form_list_orders.html", form=form, template="form-template")


@app.route("/product/<int:customer_id>")
@swag_from("swagger/product.yml")
def product(customer_id):
    return jsonify({"products": dbman.get_customer_products(customer_id)})


@app.route("/create_order", methods=["GET", "POST"])
@swag_from("swagger/create_order.yml", methods=['GET'])
def create_order():
    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        delivery_address = request.form["delivery_address"]
        creation_date = request.form["creation_date"]
        product_quantity = [
            (int(request.form[f"product_id_{i}"]), int(request.form[f"quantity_{i}"]))
            for i in range(1, 6)
            if request.form[f"quantity_{i}"] != ""
        ]
        order_id = dbman.query_create_order(
            [customer_id, delivery_address, creation_date, product_quantity]
        )
        edate = datetime.date.today()
        bdate = edate - datetime.timedelta(days=1)
        customer_orders = dbman.get_customer_orders(
            customer_id, bdate.strftime("%Y-%m-%d"), edate.strftime("%Y-%m-%d")
        )
        return render_template(
            "order_summary.html",
            template="form-template",
            customer_orders=[customer_orders[-1]],
        )
    else:
        print(request.args)
        customer_id = int(request.args.get("customer_id"))
        delivery_address = request.args.get("delivery_address")
        creation_date = request.args.get("creation_date")
        product_quantity = [
            (
                int(request.args.get(f"product_id_{i}")),
                int(request.args.get(f"quantity_{i}")),
            )
            for i in range(1, 6)
            if f"quantity_{i}" in request.args != ""
        ]
        print("funciona")
        order_id = dbman.query_create_order(
            [customer_id, delivery_address, creation_date, product_quantity]
        )
        return jsonify(order_id)


@app.route("/form_create_order")
def form_create_order():
    form = CreateForm()
    return render_template("form_create_order.html", form=form, template="form-template")


if __name__ == "__main__":
    app.run(host=settings["host"], port=settings["port"], debug=True)
