from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# mysql database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cara_ecommerce'
db = SQLAlchemy(app)


class Products(db.Model):
    __tablename__ = 'products' #table name
    product_key  = db.Column(db.String(5000), primary_key=True)
    category = db.Column(db.String(120), nullable=False)
    product_title  = db.Column(db.String(5000), nullable=False)
    price  = db.Column(db.String(50), nullable=False)
    size  = db.Column(db.String(50), nullable=False)
    stock  = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(15000), nullable=False)

@app.route("/")
def home():
    custom = ["Home", True]
    products = Products.query.filter_by().all()
    products = products*4
    fp = products[0:8]
    products.reverse()
    na = products[0:8]
    image = "images/products/f1"
    return render_template("index.html", custom=custom, fp=fp, na=na, image=image)

@app.route("/shop")
def shop():
    custom = ["Shop", True]
    products = Products.query.filter_by().all()
    products = products*4
    return render_template("shop.html", custom=custom, products=products)

@app.route("/blog")
def blog():
    custom = ["Blog", True]
    return render_template("blog.html", custom=custom)

@app.route("/about")
def about():
    custom = ["About", True]
    return render_template("about.html", custom=custom)

@app.route("/contact")
def contact():
    custom = ["Contact", True]
    return render_template("contact.html", custom=custom)

@app.route("/login")
def login():
    return render_template("login/login.html")

@app.route("/signin")
def signin():
    return render_template("login/signin.html")


app.run(debug=True)