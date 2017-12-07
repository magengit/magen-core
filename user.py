# coding=utf-8
"""
User blah blah
"""

from pymongo import MongoClient
from flask import Flask, request, render_template
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

m_client = MongoClient()
db = m_client.get_database('test_reg_users')
users = db.get_collection('users')

app = Flask(__name__)
app.template_folder = 'templates'
CsrfProtect(app)


def insert(user_data: dict):
    """insert user into db"""
    result = users.insert_one(user_data.copy())
    return result.acknowledged and result.inserted_id


def select_user_by_email(email: str):
    """select a user by email"""
    result = users.find_one(dict(email=email))
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


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Registration of a user"""
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user_dict = dict(
            email=form.email.data,
            password=form.password.data
        )
        insert(user_dict)

        return 'Hello, User'

    print('password incorrect')
    return render_template('base.html', form=form)


if __name__ == "__main__":
    app.secret_key = 'test'
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = 'test'
    app.run('0.0.0.0', port=5000)
