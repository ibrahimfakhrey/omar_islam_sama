from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import user
from sqlalchemy.testing import db
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table
    user = Paid_user.query.get(int(user_id))
    if user:
        return user
    # If not, check if user is in free_user table

    # If user is not in either table, return None
    return None

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    class Paid_user(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        email=db.Column(db.String(100))
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        Paid_user = db.Column(db.String(100), unique=True, nullable=False)
        Results = db.Column(db.String(100), nullable=False)
        News = db.Column(db.String(100))
        Discounts = db.Column(db.String(100))
        Results_done = db.Column(db.String(100))
    db.create_all()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        password = request.form.get('password')
        phone = request.form.get('number')
        user = Paid_user.query.filter_by(phone=phone).first()
        if not user:
            flash("That email does not exist, please try again.")

            # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')

            # Email exists and password correct
        else:
            login_user(user)

            return redirect("/dash")
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the registration logic here

        # After successful registration, redirect the user to the login page
        return redirect(url_for('login'))

    # If it's a GET request, simply render the register.html template
    return render_template('register.html')








if __name__ == '__main__':
    app.run()

