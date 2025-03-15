from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from forms import SignUpForm, SignInForm
from extensions import app, db

def verify_password(stored_hash, input_password):
    try:
        result = check_password_hash(stored_hash, input_password)
        return result
    except ValueError as e:
        print(f"Verification error: {e}")
        return False

class AuthController:
    def __init__(self):
        self.register_routes()

    def register_routes(self):
        app.add_url_rule("/signup", "SignUp", self.SignUp, methods=['GET', 'POST'])
        app.add_url_rule("/login", "Login", self.Login, methods=['GET', 'POST'])
        app.add_url_rule("/logout", "Logout", self.Logout, methods=['POST'])

    def SignUp(self):
        form = SignUpForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = form.name.data
                email = form.email.data
                password = form.password.data
                
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash('Error, user already exists', 'error')
                    return redirect(url_for('SignUp'))
                
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = User(
                    name=name,
                    email=email,
                    password=hashed_password
                )
                db.session.add(new_user)
                db.session.commit()
                
                flash('Registration successful!', 'success')
                return redirect(url_for('Login'))
        return render_template('auth/signup.html', form=form)

    def Login(self):
        form = SignInForm()
        if request.method == 'POST':
            #print(f"Form submitted: {request.form}")  # دیباگ فرم
            if form.validate_on_submit():
                email = form.email.data
                password = form.password.data
               # print(f"Email: {email}, Password: {password}")  # دیباگ
                next_query_param = form.next.data if 'next' in form else None
                
                user = User.query.filter_by(email=email).first()
                if user:
                    if verify_password(user.password, password):
                        login_user(user)
                        flash('Login successful!', 'success')
                        # هدایت بر اساس نقش کاربر
                        if user.admin:
                             print(f"User {user.email} is admin, redirecting to /admin")  # دیباگ
                             return redirect(url_for('index'))  # به /admin در AdminController
                        else:
                             print(f"User {user.email} is not admin, redirecting to /panel")  # دیباگ
                             return redirect(next_query_param or url_for('Panel'))  # به /panel
                    else:
                         flash('Wrong password', 'error')
                         return redirect(url_for('Login'))
                else:
                    flash('User not found', 'error')
                    return redirect(url_for('Login'))
            else:
               # print(f"Form validation failed: {form.errors}")  # دیباگ خطاهای فرم
                flash('Form validation failed', 'error')
        return render_template('auth/login.html', form=form)

    def Logout(self):
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('Login'))