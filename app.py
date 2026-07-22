from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder=".")

app.secret_key = "yasin_store_secret"


# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



# Product Model
class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )



with app.app_context():
    db.create_all()



# Home Page
@app.route("/")
def index():

    products = Product.query.all()

    return render_template(
        "index.html",
        products=products
    )



# Product Page
@app.route("/product/<int:id>")
def product(id):

    product = Product.query.get_or_404(id)

    return render_template(
        "product.html",
        product=product
    )



# Login
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        if username == "admin" and password == "1234":

            session["admin"] = True

            return redirect("/admin")


    return render_template("login.html")



# Admin Panel
@app.route("/admin")
def admin():

    if "admin" not in session:

        return redirect("/login")


    products = Product.query.all()


    return render_template(
        "admin.html",
        products=products
    )



# Add Product
@app.route("/add", methods=["POST"])
def add():

    if "admin" not in session:

        return redirect("/login")


    product = Product(

        name=request.form["name"],

        price=request.form["price"],

        description=request.form["description"]

    )


    db.session.add(product)

    db.session.commit()


    return redirect("/admin")



# Delete Product
@app.route("/delete/<int:id>")
def delete(id):

    if "admin" not in session:

        return redirect("/login")


    product = Product.query.get_or_404(id)


    db.session.delete(product)

    db.session.commit()


    return redirect("/admin")



# Edit Product
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    if "admin" not in session:

        return redirect("/login")


    product = Product.query.get_or_404(id)


    if request.method == "POST":

        product.name = request.form["name"]

        product.price = request.form["price"]

        product.description = request.form["description"]


        db.session.commit()


        return redirect("/admin")


    return render_template(
        "edit.html",
        product=product
    )



# Logout
@app.route("/logout")
def logout():

    session.pop(
        "admin",
        None
    )

    return redirect("/")



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
