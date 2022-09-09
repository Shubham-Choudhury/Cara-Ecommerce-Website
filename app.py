# from urllib import request
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secret-key'

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

class Users(db.Model):
    __tablename__ = 'users' #table name
    name = db.Column(db.String(15000), nullable=False)
    email  = db.Column(db.String(500), primary_key=True)
    password  = db.Column(db.String(20000), nullable=False)

@app.route("/")
def home():
    custom = ["Home", True]
    products = Products.query.filter_by().all()
    # products = products*4
    fp = products[0:8]
    products.reverse()
    na = products[0:8]
    image = 'f1.jpg'
    return render_template("index.html", custom=custom, fp=fp, na=na, image=image)

@app.route("/shop")
def shop():
    custom = ["Shop", True]
    products = Products.query.filter_by().all()
    # products = products*4
    return render_template("shop.html", custom=custom, products=products)

@app.route("/shop/<string:product_key>")
def product(product_key):
    custom = ["Product", True]
    product = Products.query.filter_by(product_key=product_key).first()
    images = {
        'main': '''product_images/''' + product.category + '-main' + '.jpg',
        '1': '''product_images/''' + product.category + '-1' + '.jpg',
        '2': '''product_images/''' + product.category + '-2' + '.jpg',
        '3': '''product_images/''' + product.category + '-3' + '.jpg',
    }
    
    sizes = product.size.split('-')
    print(sizes)
    return render_template("product.html", custom = custom, product=product, images=images, sizes=sizes)

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

def checkEmail(user_id):
    result = Users.query.with_entities(Users.email).all()
    # print(result)
    for i in range(len(result)):
        if(user_id in result[i][0]):
            return True
    return False

def auth(user, password):
    if(checkEmail(user)):
        result = Users.query.with_entities(Users.password).filter_by(email=user).all()
        return check_password_hash(result[0][0], password)
    return False

def sessionUser(session_user):
    result = Users.query.with_entities(Users.email).all()
    for i in range(len(result)):
        if(session_user in result[i][0]):
            return True
    return False

@app.route("/login", methods=['GET', 'POST'])
def login():
    if('user' in session and sessionUser(session['user'])):
        return redirect('/')

    if(request.method == "POST"):
        user = request.form.get('user')
        password = request.form.get('pass')
        if(auth(user, password)):
            session['user'] = user
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid Credentials")
        
    
    # print(result[0][0])
    return render_template("login/login.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if(request.method == "POST"):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        hashed_password = generate_password_hash(password)

        user = Users( name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

    return render_template("login/signin.html")


@app.route("/cart")
def cart():
    custom = ["Cart", True]
    if('user' in session and sessionUser(session['user'])):
        return render_template('user/cart.html', custom=custom)

    return redirect('/login')


@app.route("/logout")
def logout():
    if('user' in session and sessionUser(session['user'])):  
        session.pop('user')
        return redirect('/')
    
    return redirect('/login')


app.run(debug=True)