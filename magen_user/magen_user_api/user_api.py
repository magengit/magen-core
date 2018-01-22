# coding=utf-8
"""
User API module for Registration and Login
"""
import datetime
import hashlib
from http import HTTPStatus

import flask
import itsdangerous
from flask_login import login_required, login_user
from flask_wtf import FlaskForm
from magen_gmail_client_api import gmail_client
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

import magen_user_api.config as config
from magen_user_api import db
from magen_user_api.user_model import UserModel, generate_salt

__copyright__ = "Copyright(c) 2018, Cisco Systems, Inc."
__status__ = "alpha"

# creating blueprints
users_bp = flask.Blueprint('users_bp', __name__)
main_bp = flask.Blueprint('main_bp', __name__)


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
        with db.connect(config.DEV_DB_NAME) as db_instance:
            result = UserModel.select_by_email(db_instance, self.email.data)
        if not result.success:
            if result.code == config.EXISTING_EMAIL_CODE_ERR:
                self.email.errors.append("Email already registered")
            return False
        return True


class LoginForm(FlaskForm):
    """ Class represents Login Form for user """
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


def generate_confirmation_token(email):
    """
    Generate confirmation token from user email using itsdangerous

    :param email: user email
    :type email: str

    :return: generated token
    :rtype: str
    """
    serializer = itsdangerous.URLSafeTimedSerializer(config.app.config['SECRET_KEY'] )
    return serializer.dumps(email, salt=config.app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    """
    Retrieve user email from a given token

    :param token: confirmation token
    :type token: str
    :param expiration: token time of life
    :type expiration: int

    :return: email or False
    :rtype: str or bool
    """
    serializer = itsdangerous.URLSafeTimedSerializer(config.app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=config.app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except itsdangerous.BadSignature as err:
        print(err)
        return False
    return email


def check_password_hash(pw_hash, salt, password):
    """

    :param pw_hash:
    :param salt:
    :param password:
    :return:
    """
    password_hash = hashlib.pbkdf2_hmac(config.HASH_FUNCTION, password, salt.encode('utf-8'), config.ITERATIONS)
    password_double_hash = hashlib.pbkdf2_hmac(config.HASH_FUNCTION, password_hash,
                                               salt.encode('utf-8'), config.ITERATIONS).hex()
    if pw_hash == password_double_hash:
        return True
    return False


def send_confirmation(user_email):
    """
    Send confirmation letter to a new registered user

    :param user_email: user email
    :type user_email: str

    :return: None
    :rtype: void
    """
    token = generate_confirmation_token(user_email)
    confirm_url = flask.url_for('users_bp.confirm_email', token=token, _external=True)
    html = flask.render_template('email_confirmation.html', confirm_url=confirm_url, user_email=user_email)

    msg = gmail_client.create_message(
        sender=config.AUTO_SENDER,
        to=user_email,
        subject='User Registration Confirmation',
        text_part='Please confirm your e-mail address',
        html_part=html
    )
    # For now we will ignore email confirmation errors
    try:
        with gmail_client.connect() as gmail_service:
            gmail_client.send_message(gmail_service, msg)
    except FileNotFoundError as err:
        print(err.args[0])
    finally:
        return msg


@users_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """ Registration of a user """
    form = RegistrationForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            salt = generate_salt()
            hash_password = hashlib.pbkdf2_hmac(config.HASH_FUNCTION, form.password.data.encode('utf-8'),
                                                salt.encode('utf-8'), config.ITERATIONS)
            password = hashlib.pbkdf2_hmac(config.HASH_FUNCTION, hash_password,
                                           salt.encode('utf-8'), config.ITERATIONS).hex()
            # Here goes additional stuff from the form
            user_data = {}
            with db.connect(config.DEV_DB_NAME) as db_instance:
                user = UserModel(db_instance, email, password, salt, **user_data)
                result = user.submit()
            if result.success:
                send_confirmation(email)
                flask.flash('A confirmation email has been sent via email.', 'success')
                return flask.redirect(flask.url_for('main_bp.home'))
            else:
                flask.flash('Failed to insert document')
                return flask.render_template('registration.html', form=form)
    return flask.render_template('registration.html', form=form)


@users_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """ Login for the user by email and password provided to Login Form """
    form = LoginForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            with db.connect(config.DEV_DB_NAME) as db_instance:
                result = UserModel.select_by_email(db_instance, str(form.email.data))
            if result.count:
                user = result.documents
                if check_password_hash(user.password, user.salt, form.password.data.encode('utf-8')):
                    login_user(user)
                    flask.flash('Welcome.', 'success')
                    user._is_authenticated = True
                    user.submit()
                    return flask.redirect(flask.url_for('main_bp.home'))
                else:
                    flask.flash('Invalid email and/or password.', 'danger')
                    return flask.render_template('login.html', form=form), HTTPStatus.FORBIDDEN
            else:
                flask.flash('Invalid email and/or password.', 'danger')
                return flask.render_template('login.html', form=form), HTTPStatus.FORBIDDEN
    return flask.render_template('login.html', form=form)


@main_bp.route('/')
@login_required
def home():
    """ Index page """
    return flask.render_template('index.html')


@users_bp.route('/confirm/<token>')
def confirm_email(token):
    """

    :param token:
    :return:
    """
    email = confirm_token(token)
    if not email:
        flask.flash('Confirmation link is invalid or has expired')
        return flask.redirect(flask.url_for('main_bp.home'))
    with db.connect(db_name=config.DEV_DB_NAME) as db_instance:
        result = UserModel.select_by_email(db_instance, email)
    if result.count:
        user = result.documents
        if user.confirmed:
            flask.flash('User is already confirmed, please login')
            return flask.redirect(flask.url_for('user_bp.login'))
        user._is_authenticated = True
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        user.submit()
        login_user(user)
        flask.flash('You have confirmed your account. Thanks!', 'success')
    return flask.redirect(flask.url_for('main_bp.home'))


@config.login_manager.user_loader
def load_user(user_id):
    """

    :param user_id:
    :return:
    """
    with db.connect(config.DEV_DB_NAME) as db_instance:
        result = UserModel.select_by_email(db_instance, user_id)
    if result.count:
        user = result.documents
        return user
    return None


if __name__ == "__main__":
    config.app.register_blueprint(users_bp)
    config.app.register_blueprint(main_bp)
    config.app.run('0.0.0.0', port=5005)

