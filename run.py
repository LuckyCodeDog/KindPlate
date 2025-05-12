# app.py

from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from app import create_app
from app.common.forms import BookingForm
from app.models.restaurant_profile import RestaurantProfile

app = create_app()

#error handling
@app.errorhandler(404)
def page_not_found(e):
    error_message = str(e)
    return render_template('404.html', error_message=error_message), 404

@app.context_processor
def inject_restaurant_profile():
    restaurant_profile = RestaurantProfile.query.first()
    opening = restaurant_profile.opening_time
    closing = restaurant_profile.closing_time

    today = datetime.today()
    opening_dt = datetime.combine(today, opening)
    closing_dt = datetime.combine(today, closing)

    # 每隔30分钟生成一个时间段
    time_slots = []
    while opening_dt <= closing_dt:
        time_slots.append(opening_dt.strftime("%H:%M"))
        opening_dt += timedelta(minutes=30)

    return dict(restaurant_profile=restaurant_profile, time_slots=time_slots)

@app.context_processor
def inject_booking_form():
    return {'booking_form': BookingForm()}
@app.errorhandler(500)
def page_not_found(e):
    error_message = str(e)
    return render_template('500.html', error_message=error_message), 500

if __name__ == '__main__':
    app.run(debug=True)
