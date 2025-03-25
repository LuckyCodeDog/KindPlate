from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, FileField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileAllowed
from flask import current_app
from app.common.MyEnum import Role
class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = SelectField('Category', choices=[('appetizer', 'Appetizer'), ('main_course', 'Main Course'), ('dessert', 'Dessert'), ('drink', 'Drink')], validators=[Optional()])
    available = BooleanField('Available', default=True)
    image = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])


class UserForm(FlaskForm):

    
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=100)])

    phone_number = StringField('Phone Number', validators=[Length(max=20)])

    role = SelectField('Role', choices=[(role.name, role.value) for role in Role], coerce=str, validators=[DataRequired()])

    first_name = StringField('First Name', validators=[Length(max=50)])

    last_name = StringField('Last Name', validators=[Length(max=50)])

    contribution = StringField('Contribution', default='0.00')

    image = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    
    status = SelectField('Status', choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
