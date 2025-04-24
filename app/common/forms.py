from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, StringField, TextAreaField, DecimalField, SelectField, BooleanField, FileField, PasswordField, EmailField, SubmitField, TimeField
from wtforms.validators import DataRequired, Optional, NumberRange
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileAllowed
from flask import current_app
from app.common.MyEnum import PaymentMethod, Role
class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    category = SelectField('Category', choices=[('appetizer', 'Appetizer'), ('main_course', 'Main Course'), ('dessert', 'Dessert'), ('drink', 'Drink')], validators=[Optional()])
    available = BooleanField('Available', default=True)
    image = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])


class UserForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=100)])

    phone_number = StringField('Phone Number', validators=[Length(max=20)])

    role = SelectField('Role', choices=[(role.name, role.value) for role in Role], coerce=str, validators=[DataRequired()])

    first_name = StringField('First Name', validators=[Length(max=50)])

    last_name = StringField('Last Name', validators=[Length(max=50)])

    contribution = StringField('Contribution', default='0.00')

    image = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    
    status = SelectField('Status', choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')


class UserEditForm(FlaskForm):
    
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=100)])

    phone_number = StringField('Phone Number', validators=[Length(max=20)])

    role = SelectField('Role', choices=[(role.name, role.value) for role in Role], coerce=str, validators=[DataRequired()])

    first_name = StringField('First Name', validators=[Length(max=50)])

    last_name = StringField('Last Name', validators=[Length(max=50)])

    contribution = StringField('Contribution', default='0.00')

    image = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    
    status = SelectField('Status', choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')


class changePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=50)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if self.new_password.data != self.confirm_password.data:
            self.confirm_password.errors.append('Passwords must match')
            return False

        return True
    

class RestaurantProfileForm(FlaskForm):
    description = TextAreaField('Description', validators=[Optional()])
    rating = DecimalField('Rating', places=2, validators=[Optional(), NumberRange(min=0, max=5)])
    image = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    facilities = TextAreaField('Facilities', validators=[Optional()])
    opening_date = DateField('Opening Date', validators=[Optional()])
    opening_time = TimeField('Opening Time', validators=[Optional()])
    closing_time = TimeField('Closing Time', validators=[Optional()])
    submit = SubmitField('Submit')


class CheckoutForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    address2 = StringField('Address 2', validators=[Length(max=100)])
    city = StringField('City/Town', validators=[DataRequired(), Length(max=50)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[Length(max=500)])

    payment_method = RadioField(
        'Payment Method',
        choices=[(method.value, method.name.replace('_', ' ').title()) for method in PaymentMethod],
        validators=[DataRequired()]
    )

    submit = SubmitField('Place Order')
