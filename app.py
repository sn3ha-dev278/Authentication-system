from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


app.config['SECRET_KEY'] = os.urandom(32)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )



class RegisterForm(FlaskForm):

    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"}
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"}
    )

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = User.query.filter_by(
            username=username.data).first()

        if existing_user:
            raise ValidationError(
                'That username already exists.'
            )


class LoginForm(FlaskForm):

    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"}
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"}
    )

    submit = SubmitField('Login')



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("3 per 5 minutes")
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data).first()

        if user and bcrypt.check_password_hash(
                user.password, form.password.data):

            login_user(user)
            return redirect(url_for('dashboard'))

        flash("Invalid username or password")

    return render_template('login.html', form=form)


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("rate_limit.html"), 429



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        new_user = User(
            username=form.username.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)