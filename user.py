# coding=utf-8
"""
User blah blah
"""

from pymongo import MongoClient
from flask import Flask, Blueprint, request, render_template, flash, url_for, redirect
from flask_login import LoginManager, login_required, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from itsdangerous import URLSafeTimedSerializer
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt

# connecting to DB
m_client = MongoClient()
db = m_client.get_database('test_reg_users')
users = db.get_collection('users')

# creating blueprints
users_bp = Blueprint('users_bp', __name__)
main_bp = Blueprint('main_bp', __name__)

# creating flask App
app = Flask(__name__)
app.template_folder = 'templates'  # providing path to template folder
# configuring application with CSRF protection for form security
CSRFProtect(app)

# configuring application with LoginManger for @login_required and handling login requests
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users_bp.login'

# configuring application with Bcrypt to provide hashing utilities for application
# like generating hash for password and check hash
bcrypt = Bcrypt(app)


def insert(user_data: dict):
    """insert user into db"""
    result = users.insert_one(user_data.copy())
    return result.acknowledged and result.inserted_id


def select_user_by_email(email: str):
    """select a user by email"""
    result = users.find_one(dict(email=email), {'_id': False})
    return result


class RegistrationForm(FlaskForm):
    """Class represents Registration Form for user"""
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        """Validate that user has unique email"""
        initial_validation = super(RegistrationForm, self).validate()
        if not initial_validation:
            return False
        found = select_user_by_email(self.email.data)
        if found:
            self.email.errors.append("Email already registered")
            return False
        return True


class LoginForm(FlaskForm):
    """Class represents Login Form for user"""
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


@users_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """Registration of a user"""
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user_dict = dict(
            email=form.email.data,
            password=form.password.data,
            confirmed=False
        )
        insert(user_dict)
        token = generate_confirmation_token(user_dict['email'])

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for('main_bp.home'))

    print('password incorrect')
    return render_template('base.html', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = select_user_by_email(email=form.email.data)
        if user and bcrypt.check_password_hash(
                user['password'], request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main_bp.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            # TODO: create a login.html template and change index.html to login.html
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@main_bp.route('/')
@login_required
def home():
    """Index page"""
    return render_template('index.html')


if __name__ == "__main__":
    app.secret_key = 'test_key'
    # TODO: Configuration should be provided through ENV
    app.config['WTF_CSRF_ENABLED'] = True
    # app.config['WTF_CSRF_SECRET_KEY'] = 'test'
    app.config['SECRETE_KEY'] = 'test_key'
    app.config['SECURITY_PASSWORD_SALT'] = 'test_salt'
    app.register_blueprint(users_bp)
    app.register_blueprint(main_bp)
    app.run('0.0.0.0', port=5000)

