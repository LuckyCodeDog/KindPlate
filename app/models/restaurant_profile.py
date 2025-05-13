import datetime
from app.extensions import db
from sqlalchemy import Column, Integer, Text, DECIMAL, String, Date, Time, JSON, TIMESTAMP, func


class RestaurantProfile(db.Model):
    __tablename__ = 'restaurant_profile'
    
    profile_id = db.Column(Integer, primary_key=True, autoincrement=True)
    description = db.Column(Text)
    story = db.Column(Text)
    rating = db.Column(DECIMAL(3, 2), default=0.00)
    image_url = db.Column(String(255))
    facilities = db.Column(Text)
    opening_date = db.Column(Date)
    opening_time = db.Column(Time)
    closing_time = db.Column(Time)
    created_at = db.Column(TIMESTAMP, server_default=func.now())
    updated_at = db.Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


    @staticmethod
    def get_all_profiles():
        return RestaurantProfile.query.all()

    @staticmethod
    def get_profile_by_id(profile_id):
        return RestaurantProfile.query.get(profile_id)

    @staticmethod
    def create_profile(description=None, story=None, rating=0.0, image_url=None,
                       facilities=None, opening_date=None, opening_time=None,
                       closing_time=None, social_media_links=None):
        new_profile = RestaurantProfile(
            description=description,
            story=story,
            rating=rating,
            image_url=image_url,
            facilities=facilities,
            opening_date=opening_date,
            opening_time=opening_time,
            closing_time=closing_time,
            social_media_links=social_media_links
        )
        db.session.add(new_profile)
        db.session.commit()
        return new_profile

    @staticmethod
    def update_profile(profile_id, description=None, story=None, rating=None, image_url=None,
                       facilities=None, opening_date=None, opening_time=None, closing_time=None):
        profile = RestaurantProfile.query.get(profile_id)
        if profile:
            if description is not None:
                profile.description = description
            if rating is not None:
                profile.rating = rating
            if image_url is not None:
                profile.image_url = image_url
            if facilities is not None:
                profile.facilities = facilities
            if opening_date is not None:
                profile.opening_date = opening_date
            if opening_time is not None:
                profile.opening_time = opening_time
            if closing_time is not None:
                profile.closing_time = closing_time
            if story is not None:
                profile.story = story


            profile.updated_at = datetime.datetime.now()  
            db.session.commit()
            return profile
        return None

    @staticmethod
    def delete_profile(profile_id):
        profile = RestaurantProfile.query.get(profile_id)
        if profile:
            db.session.delete(profile)
            db.session.commit()
            return True
        return False