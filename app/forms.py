from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RideForm(FlaskForm):
    pickup_location = StringField('Pickup Location', validators=[DataRequired()])
    dropoff_location = StringField('Dropoff Location', validators=[DataRequired()])
    tariff = SelectField('Tariff', choices=[('economy', 'Economy'), ('comfort', 'Comfort'), ('business', 'Business')], validators=[DataRequired()])
    submit = SubmitField('Book Ride')
