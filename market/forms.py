from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import Length , EqualTo , Email ,DataRequired , ValidationError
from market.models import User


class RegisterForm(FlaskForm) : 
    def validate_username(self , username_to_check) : 
        user = User.query.filter_by(username=username_to_check.data).first()
        if user : 
            raise ValidationError('Username already exist , try with another username')
    
    def validate_email_address(self , email_address_to_check) : 
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email : 
            raise ValidationError('Email already exist , try with another email ')
    username = StringField(label='User Name' , validators=[Length(min=2, max=30) , DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email() , DataRequired()])
    password1 = PasswordField(label='Password',  validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password' , validators=[EqualTo('password1') , DataRequired()])
    submit = SubmitField(label='submit')
    
class LoginForm(FlaskForm) : 
    username = StringField(label='UserName',validators=[DataRequired()])
    password = PasswordField(label="Password" , validators=[DataRequired()])
    submit = SubmitField(label="signin")
    
class PurchassForm(FlaskForm) : 
    submit = SubmitField(label='submit')
    
class SellForm(FlaskForm) : 
    submit = SubmitField(label="submit")