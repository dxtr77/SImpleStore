from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisismysecretkey'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(30), nullable = False)
    create_at = db.Column(db.String(30), nullable = False)
    edited_at = db.Column(db.String(30), nullable = False)


class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    price = db.Column(db.String(100), nullable = False)
    owner_id = db.Column(db.String(100), nullable = False)
    category = db.Column(db.String(30), nullable = False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('/login.html')


@app.route('/register')
def register():
    return render_template('/register.html')


if __name__ == "__main__":
    app.run(debug=True)
