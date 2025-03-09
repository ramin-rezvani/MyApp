from flask_wtf import FlaskForm,RecaptchaField
 
from wtforms import StringField, PasswordField, SubmitField,EmailField
from wtforms.validators import DataRequired, Length,Email,EqualTo


class SignUpForm(FlaskForm):
    name = StringField("name ",validators=[DataRequired("name field is required.")])
    email = EmailField("email",validators=[DataRequired('email is requaired'),Email('email is invalid')])
    password = PasswordField("password",validators=[DataRequired("password  required."),
                                                      Length(min=6, message="password least 6 characters .")])
    confirm=PasswordField('confirm password ',validators=[EqualTo('password',message='password is not confirmed.')])
    recaptcha=RecaptchaField()
    
        
class SignInForm(FlaskForm):
    email = EmailField("email",validators=[DataRequired('email is requaired'),Email('email is invalid')])
    password = PasswordField("password",validators=[DataRequired("password  required."),
                                                      Length(min=6, message="password least 6 characters .")])
    recaptcha=RecaptchaField()
    