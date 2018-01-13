# coding=utf-8
"""
User blah blah
"""
import datetime
from flask import Flask, Blueprint, request, render_template, flash, url_for, redirect
from flask_login import LoginManager, login_required, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from itsdangerous import URLSafeTimedSerializer
from flask_wtf import CSRFProtect
import hashlib

import db
from user_model import UserModel, generate_salt
from config import DEV_DB_NAME, EXISTING_EMAIL_CODE_ERR, AUTO_SENDER

from magen_gmail_client_api import gmail_client

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

# Initializing hash function and iterations for Pbkdf2 hashing
HASH_FUNCTION = 'sha256'
ITERATIONS = 100000


class RegistrationForm(FlaskForm):
    """ Class represents Registration Form for user """
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
        """ Validate that user has unique email """
        initial_validation = super(RegistrationForm, self).validate()
        if not initial_validation:
            return False
        with db.connect(DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, self.email.data)
        if not result.success:
            if result.code == EXISTING_EMAIL_CODE_ERR:
                self.email.errors.append("Email already registered")
            return False
        return True


class LoginForm(FlaskForm):
    """ Class represents Login Form for user """
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


def generate_confirmation_token(email):  # skip in tests for now
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):  # skip in tests for now
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


def check_password_hash(pw_hash, salt, password):
    password_hash = hashlib.pbkdf2_hmac(HASH_FUNCTION, password, salt.encode('utf-8'), ITERATIONS)
    password_double_hash = hashlib.pbkdf2_hmac(HASH_FUNCTION, password_hash,
                                               salt.encode('utf-8'), ITERATIONS).hex()
    if pw_hash == password_double_hash:
        return True
    return False


@users_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """Registration of a user"""
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            salt = generate_salt()
            hash_password = hashlib.pbkdf2_hmac(HASH_FUNCTION, form.password.data.encode('utf-8'),
                                                salt.encode('utf-8'), ITERATIONS)
            password = hashlib.pbkdf2_hmac(HASH_FUNCTION, hash_password,
                                           salt.encode('utf-8'), ITERATIONS).hex()
            # Here goes additional stuff from the form
            user_data = {}
            with db.connect(DEV_DB_NAME) as db_instance:
                user = UserModel(db_instance, email, password, salt, **user_data)
                result = user.submit()
            if result.success:
                token = generate_confirmation_token(email)
                confirm_url = url_for('users_bp.confirm_email', token=token, _external=True)
                html = render_template('email_confirmation.html', confirm_url=confirm_url, user_email=email)

                msg = gmail_client.create_message(
                    sender=AUTO_SENDER,
                    to=email,
                    subject='User Registration Confirmation',
                    text_part='Please confirm your e-mail address',
                    html_part=html
                )

                with gmail_client.connect() as gmail_service:
                    gmail_client.send_message(gmail_service, 'me', msg)
                flash('A confirmation email has been sent via email.', 'success')
                return redirect(url_for('main_bp.home'))
            else:
                flash('Failed to insert document')
                return render_template('registration.html', form=form)
                  
        flash('password incorrect')
    return render_template('registration.html', form=form)


@users_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """ Login for the user by email and password provided to Login Form """
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            with db.connect(DEV_DB_NAME) as db_instance:
                result = UserModel.select_by_email(db_instance, str(form.email.data))
            if result.count:
                user = result.documents
                if check_password_hash(user.password, user.salt, form.password.data.encode('utf-8')):
                    login_user(user)
                    flash('Welcome.', 'success')
                    user._is_authenticated = True
                    user.submit()
                    return redirect(url_for('main_bp.home'))
                else:
                    flash('Invalid email and/or password.', 'danger')
                    return render_template('login.html', form=form), 403
            else:
                flash('Invalid email and/or password.', 'danger')
                return render_template('login.html', form=form), 403
    return render_template('login.html', form=form)


@main_bp.route('/')
@login_required
def home():
    """Index page"""
    return render_template('index.html')


@users_bp.route('/confirm/<token>')
def confirm_email(token):
    """

    :param token:
    :return:
    """
    email = confirm_token(token)
    if not email:
        flash('Confirmation link is invalid or has expired')
        return redirect(url_for('main_bp.home'))
    with db.connect(db_name=DEV_DB_NAME) as db_instance:
        result = UserModel.select_by_email(db_instance, email)
    if result.count:
        user = result.documents
        if user.confirmed:
            flash('User is already confirmed, please login')
            return redirect(url_for('user_bp.login'))
        user._is_authenticated = True
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        user.submit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main_bp.home'))


@login_manager.user_loader
def load_user(user_id):
    with db.connect(DEV_DB_NAME) as db_instance:
        result = UserModel.select_by_email(db_instance, user_id)
    if result.count:
        user = result.documents
        return user
    return None


if __name__ == "__main__":
    app.secret_key = 'test_key'
    # TODO: Configuration should be provided through ENV
    app.config['WTF_CSRF_ENABLED'] = True
    # app.config['WTF_CSRF_SECRET_KEY'] = 'test'
    app.config['SECRET_KEY'] = 'test_key'
    app.config['SECURITY_PASSWORD_SALT'] = 'test_salt'
    app.register_blueprint(users_bp)
    app.register_blueprint(main_bp)
    app.run('0.0.0.0', port=5005)

