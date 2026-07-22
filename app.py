
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"

products = [
    {
        "id": 1,
        "name": "پکیج ربات تلگرام",
        "price": "200000 تومان",
        "description": "ربات آماده تلگرام"
    }
]


@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")


@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    return render_template("admin.html", products=products)


@app.route("/delete/<int:id>")
def delete(id):

    global products

    products = [
        p for p in products if p["id"] != id
    ]

    return redirect("/admin")


@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    for p in products:
        if p["id"] == id:

            if request.method == "POST":
                p["name"] = request.form["name"]
                p["price"] = request.form["price"]

                return redirect("/admin")

            return render_template("edit.html", product=p)


app.run(host="0.0.0.0", port=5000)
