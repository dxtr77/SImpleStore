from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators
from wtforms.fields.choices import SelectField
from wtforms.form import Form
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello.db'  # Path to your database file
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name= db.Column(db.String(15))

    username = db.Column(db.String(15), unique=True)

    email = db.Column(db.String(50), unique=True)

    role = db.Column(db.String(50))

    password = db.Column(db.String(256))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate:

        user = User.query.filter_by(email=form.email.data).first()

        if user:

            if check_password_hash(user.password, form.password.data):

                flash('You have successfully logged in.', "success")

                session['logged_in'] = True

                session['email'] = user.email

                session['username'] = user.username

                return redirect(url_for('index'))

            else:

                flash('Username or Password Incorrect', "Danger")

                return redirect(url_for('login'))

    return render_template('login.html', form=form)


def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(

            name=form.name.data,

            username=form.username.data,

            email=form.email.data,

            password=hashed_password,

            role=form.role.data
        )

        db.session.add(new_user)

        db.session.commit()

        flash('You have successfully registered', 'success')

        return redirect(url_for('login'))

    else:

        return render_template('register.html', form=form)


class RegisterForm(Form):
    name = StringField("Name", validators=[validators.Length(min=3, max=25),
                                         validators.DataRequired(message="Please Fill This Field")])

    username = StringField("Username", validators=[validators.Length(min=3, max=25)])

    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])

    password = PasswordField("Password", validators=[

        validators.DataRequired(message="Please Fill This Field"),

        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])
    role = SelectField("Role", choices=[('admin', 'Admin'), ('seller', 'Seller')],
                       validators=[validators.DataRequired(message="Please Select a Role")])
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])


class LoginForm(Form):

    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])

    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
        app.run(debug=True)