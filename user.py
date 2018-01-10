# coding=utf-8
"""
User blah blah
"""

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
from config import DEV_DB_NAME, EXISTING_EMAIL_CODE_ERR, USER_COLLECTION_NAME

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
    password_hash = hashlib.pbkdf2_hmac(HASH_FUNCTION, password, salt.encode('utf-8'), ITERATIONS).hex()
    if pw_hash == password_hash:
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
            password = hashlib.pbkdf2_hmac(HASH_FUNCTION, form.password.data.encode('utf-8'),
                                           salt.encode('utf-8'), ITERATIONS).hex()
            user_details = dict(
                confirmed=False
            )
            with db.connect(DEV_DB_NAME) as db_instance:
                user = UserModel(db_instance, email, password, salt, **user_details)
                result = user.submit()
            if result.success:
                # TODO (for Alena): email generation
                # token = generate_confirmation_token(email)
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
                # FIXME (for Alena): correct hashing and verifying
                if check_password_hash(user.password, user.salt, form.password.data.encode('utf-8')):
                    login_user(user)
                    flash('Welcome.', 'success')
                    with db.connect(DEV_DB_NAME) as db_instance:
                        user_collection = db_instance.get_collection(USER_COLLECTION_NAME)
                        user_collection.update_one({'email': str(form.email.data)},
                                                   {"$set": {'_is_authenticated': True}})
                        user._is_authenticated = True
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


@login_manager.user_loader
def load_user(user_id):
    with db.connect(DEV_DB_NAME) as db_instance:
        user_collection = db_instance.get_collection(USER_COLLECTION_NAME)
        user = user_collection.find({"email": user_id})
    if user.count():
        for itr in user:
            if 'email' and 'password' in itr:
                email = itr['email']
                password = itr['password']
                salt = itr['salt']
                return UserModel(db_instance, email, password, salt)
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

