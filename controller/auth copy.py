from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user,login_manager,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from forms import SignUpForm, SignInForm
from extensions import app, db  # وارد کردن app و db از extensions



def verify_password(stored_hash, input_password):
    try:
        return check_password_hash(input_password, stored_hash)
    except ValueError as e:
        print(f"Verification error: {e}")
        return False
class AuthController:
    def __init__(self):
        self.register_routes()

    def register_routes(self):
        # تعریف مسیرها با استفاده از add_url_rule
        app.add_url_rule("/signup", "SignUp", self.SignUp, methods=['GET', 'POST'])
        app.add_url_rule("/login", "Login", self.Login, methods=['GET', 'POST'])
        app.add_url_rule("/logout", "Logout", self.Logout, methods=['POST'])

    
    

    def SignUp(self):
        form = SignUpForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = request.form.get('name')
                email = request.form.get('email')
                password = request.form.get('password')
                
                # بررسی وجود کاربر
                existing_user = User.query.filter_by(email=email).first()
                
                if existing_user:
                    flash('Error, user already exists', 'error')
                    return redirect(url_for('SignUp'))
                
                hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
                # ایجاد کاربر جدید
                new_user = User(
                    name=name,
                    email=email,
                    password=hashed_password
                )
                db.session.add(new_user)
                db.session.commit()
                
                flash('Registration successful!', 'success')
                return redirect(url_for('Login'))  # پس از ثبت‌نام، کاربر به صفحه لاگین هدایت می‌شود
           
        return render_template('auth/signup.html', form=form)



    def Login(self):
       form = SignInForm()
       if request.method == 'POST':
           if form.validate_on_submit():
               email = request.form.get('email')  # استفاده از form.email.data به جای request.form.get
               password = request.form.get('password')   # استفاده از form.password.data به جای request.form.get
               next_query_param = request.form.get('next')
               
               # بررسی وجود کاربر
               user = User.query.filter_by(email=email).first()
               
               if user:
                     
                 if verify_password(user.password,password):
                     login_user(user)
                     flash('Login successful!', 'success')
                     return redirect(next_query_param or url_for('Panel'))
                 else:
                     flash('Wrong password', 'error')
                     return redirect(url_for('Login'))
               else:
                   flash('User not found', 'error')
                   return redirect(url_for('Login'))
          
       return render_template('auth/login.html', form=form)

    def Logout(self):
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('Login'))  # پس از خروج، کاربر به صفحه لاگین هدایت می‌شود