from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, FileField
from wtforms.validators import DataRequired, NumberRange

class BadgeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    required_water_saved = DecimalField('Required Water Saved (liters)', 
                                      validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Badge Image') 