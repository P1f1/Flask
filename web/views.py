from flask import Flask, render_template, request, redirect, url_for
from database.models import Products, Locations, Inventory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app

engine = create_engine("mysql+mysqlconnector://root:root@localhost/testdb", echo=True)
Session = sessionmaker(engine)


@app.route("/")
def index():
    with Session() as s:
        all_product = s.query(Products.name,
                              Products.description,
                              Products.price,
                              Locations.name,
                              Inventory.quantity,
                              Inventory.product_id,
                              Inventory.location_id,
                              Products.id,
                              Inventory.id
                              ).outerjoin(Inventory, Products.id == Inventory.product_id
                                          ).outerjoin(Locations, Inventory.location_id == Locations.id
                                                      ).all()
        all_location = s.query(Locations.id, Locations.name).all()

        return render_template("index.html", all_product=all_product, all_location=all_location)


@app.route("/add_to_whs/<int:product_id>/<int:quantity>", methods=["POST"])
def add_to_whs(product_id, quantity=0):
    if request.method == "POST":
        loc_id = request.form.get("location_id")
        with Session() as s:
            product = s.query(Inventory).filter(
                Inventory.product_id == product_id, Inventory.quantity == quantity
            ).one()

            if product:
                check_prod = s.query(Inventory).filter(
                    Inventory.product_id == product_id, Inventory.location_id == loc_id
                )

                if check_prod.count() >= 1:
                    check_prod.update(
                        {"quantity": Inventory.quantity + quantity},
                        synchronize_session='fetch'
                    )
                    s.delete(product)
                    s.commit()
                else:
                    product.location_id = loc_id
                    s.commit()

    return redirect(url_for("index"))


@app.route("/del_from_whs/<int:product_id>/<int:location_id>/<int:quantity>", methods=["POST"])
def del_from_whs(product_id, location_id, quantity):
    if request.method == "POST":
        with Session() as s:
            product = s.query(Inventory).filter(
                Inventory.product_id == product_id,
                Inventory.location_id == location_id,
                Inventory.quantity == quantity
            ).one()

            if product:
                product.location_id = None
                s.commit()

    return redirect(url_for("index"))


@app.route("/add_product", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        with Session() as s:
            new_product = Products(
                name=request.form.get("name"),
                description=request.form.get("description"),
                price=request.form.get("price")
            )
            s.add(new_product)
            s.commit()

            new_product_id = new_product.id
            new_inventory = Inventory(product_id=new_product_id)
            s.add(new_inventory)
            s.commit()

    return redirect(url_for("index"))


@app.route("/add_location", methods=["POST", "GET"])
def add_location():
    if request.method == "POST":
        with Session() as s:
            new_location = Locations(name=request.form.get("name"))
            s.add(new_location)
            s.commit()

    return redirect(url_for("index"))


@app.route("/change_quantity/<int:product_id>/<int:quantity>/<int:inventory_id>", methods=["POST", "GET"])
def change_quantity(product_id, quantity, inventory_id):
    if request.method == "POST":
        with Session() as s:
            product_change = s.query(Inventory).filter(Inventory.product_id == product_id,
                                                       Inventory.quantity == quantity,
                                                       Inventory.id == inventory_id).first()
            if product_change:
                product_change.quantity = request.form.get("new_value")
                s.commit()

    return redirect(url_for("index"))
