from flask import Blueprint, render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm
from .models import User, Ride
from . import db, bcrypt


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@main.route('/order_history')
def order_history():
    rides = Ride.query.filter_by(user_id=1).all()  # Заменим user_id на текущего пользователя в будущем
    return render_template('order_history.html', rides=rides)


@main.route('/book_ride', methods=['GET', 'POST'])
def book_ride():
    form = RideForm()
    if form.validate_on_submit():
        ride = Ride(
            pickup_location=form.pickup_location.data,
            dropoff_location=form.dropoff_location.data,
            date=datetime.utcnow(),
            user_id=1  # Для простоты, пока что ставим user_id = 1 (в будущем заменим на текущего пользователя)
        )
        db.session.add(ride)
        db.session.commit()
        flash('Your ride has been booked!', 'success')
        return redirect(url_for('main.order_history'))
    return render_template('book_ride.html', form=form)
