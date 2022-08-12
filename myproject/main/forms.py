from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, length, DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(),
                                             # Regexp('[a-zA-Z0-9_]+@[a-zA-Z]+\.(com|edu|net|xyz)',
                                             #        message="bad format for the mail a good example aba@aba.com")
                                             ],
                        render_kw={'placeholder': 'Email'})
    username = StringField('Username', validators=[
        length(min=1, max=250,
               message='the username is too long try to choose a shorter one'),
        InputRequired(),
    ],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('pass_confirm', message='Passwords must match')],
                             render_kw={'placeholder': 'Password'})
    pass_confirm = PasswordField('Confirm Password',
                                 validators=[InputRequired()], render_kw={'placeholder': 'Confirm password'})

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(),
                                             # Regexp('[a-zA-Z0-9_]+@[a-zA-Z]+\.(com|edu|net|xyz)',
                                             #        message="bad format for the mail a good example aba@aba.com")
                                             ],
                        render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField("Login")
