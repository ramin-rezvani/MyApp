from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField,TextAreaField,DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired("Name field is required.")])
    email = EmailField("Email", validators=[DataRequired('Email is required'), Email('Email is invalid')])
    password = PasswordField("Password", validators=[DataRequired("Password is required."),
                                                      Length(min=6, message="Password must be at least 6 characters.")])
    confirm = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords do not match.')])
    recaptcha = RecaptchaField()
    submit = SubmitField("Sign Up")

class SignInForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired('Email is required'), Email('Email is invalid')])
    password = PasswordField("Password", validators=[DataRequired("Password is required."),
                                                      Length(min=6, message="Password must be at least 6 characters.")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Sign In")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired("Old password is required.")])
    new_password = PasswordField("New Password", validators=[DataRequired("New password is required."),
                                                             Length(min=6, message="Password must be at least 6 characters.")])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired("Confirm password is required."),
                                                                       EqualTo('new_password', message='Passwords do not match.')])
    submit = SubmitField("Change Password")
    
class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired("Name field is required.")])
    email = EmailField("Email", validators=[DataRequired("Email is required"), Email("Email is invalid")])
    submit = SubmitField("Update Profile")
    
class UploadAvatarForm(FlaskForm):
    avatar = FileField("َAvatar", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "jpg، png و jpeg only trust")])
    submit = SubmitField("Update Profile Picture")
    
class NewUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired("Name field is required.")])
    email = EmailField("Email", validators=[DataRequired('Email is required'), Email('Email is invalid')])
    password = PasswordField("Password", validators=[DataRequired("Password is required.")])
    submit = SubmitField("Add New User")
    
class CourseForm(FlaskForm):
    title=StringField("title",validators=[DataRequired('Please Enter Course Title')])
    content=TextAreaField('content',validators=[DataRequired('please enter course content')])
    
class EpisodeForm(FlaskForm):
    title = StringField('title', validators=[DataRequired('Title Field is Required')])
    content = TextAreaField('content', validators=[DataRequired('Content of Course is Required')])
    videoUrl = StringField('videoUrl', validators=[DataRequired('Video URL Field is Required')])
    time = StringField('time', validators=[DataRequired('Video time Field is Required')])
    number = DecimalField('number', validators=[DataRequired('Number Field is Required')])