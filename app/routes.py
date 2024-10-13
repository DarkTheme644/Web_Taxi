from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm, RideForm
from .models import User, Ride
from . import db, bcrypt, login_manager
from datetime import datetime

main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'danger')
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@main.route('/book_ride', methods=['GET', 'POST'])
@login_required
def book_ride():
    form = RideForm()
    if form.validate_on_submit():
        ride = Ride(
            pickup_location=form.pickup_location.data,
            dropoff_location=form.dropoff_location.data,
            tariff=form.tariff.data,
            distance=form.distance.data,
            time=form.time.data,
            cost=form.cost.data,
            date=datetime.utcnow(),
            user_id=current_user.id,
            status="Ordered"
        )
        db.session.add(ride)
        db.session.commit()
        flash('Your ride has been booked!', 'success')
        return redirect(url_for('main.order_history'))
    return render_template('book_ride.html', form=form)


@main.route('/order_history')
@login_required
def order_history():
    rides = Ride.query.filter_by(user_id=current_user.id).all()
    return render_template('order_history.html', rides=rides)


@main.route('/order_taxi', methods=['POST'])
@login_required
def order_taxi():
    data = request.get_json()
    start_location = data['start_location']
    end_location = data['end_location']
    tariff = data['tariff']
    distance = data['distance']
    time = data['time']
    cost = data['cost']

    new_ride = Ride(
        pickup_location=start_location,
        dropoff_location=end_location,
        tariff=tariff,
        distance=distance,
        time=time,
        cost=cost,
        status="Ordered",
        date=datetime.utcnow(),
        user_id=current_user.id
    )
    db.session.add(new_ride)
    db.session.commit()

    return jsonify(success=True)


@main.route('/complete_order/<int:ride_id>', methods=['POST'])
@login_required
def complete_order(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    if ride.user_id != current_user.id:
        flash('You do not have permission to complete this ride.', 'danger')
        return redirect(url_for('main.order_history'))

    ride.status = "Completed"
    db.session.commit()
    flash('Ride marked as completed.', 'success')
    return redirect(url_for('main.order_history'))
