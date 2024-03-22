from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
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


class registerForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder" : "Password"})
    role = StringField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder":"Seller/Admin"})
    submit = SubmitField("Register")


class loginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min = 4, max = 20)], render_kw={"placeholder" : "Password"})
    submit = SubmitField("Login")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    return render_template('/login.html', form = form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        # Process login logic
        return 'Logged in successfully!'
    return render_template('/register.html', form = form)


if __name__ == "__main__":
    app.run(debug=True)
