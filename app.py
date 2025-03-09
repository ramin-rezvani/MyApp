from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from extensions import db
import secrets
import os
from forms import SignUpForm,SignInForm
from flask_login import LoginManager,login_user,logout_user,current_user,logout_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#google recaptcha config
app.config['RECAPTCHA_PUBLIC_KEY']='6LeTG-4qAAAAAFeKMuo0SJHrXkJepmHtLD5MqFvi'#public key
app.config['RECAPTCHA_PRIVATE_KEY']='6LeTG-4qAAAAAAcnjWJqkTgmygBE74rPH3LW94OY'#private key

db.init_app(app)

loginmanager=LoginManager(app)
loginmanager.login_view='login'


@app.route('/')
def main():
 return render_template('home.html')

@loginmanager.user_loader
def user_loader(User_id):
    return User.query.get(User_id)

@app.route('/signup' ,methods =['GET', 'POST'])

def SignUp():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            
            #checked user exists
            query = User.query.filter_by(email=email).first()
            
            if  query :
                flash('Error, user already exists')
                return redirect(url_for('SignUp'))
            # Create a new User
            newUser = User(name=name, email=email,password=password)
                  
         
            db.session.add(newUser)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('main')) 
           
    return render_template('signup.html', form=form)


@app.route('/login' ,methods =['GET', 'POST'])

def login():
    form = SignInForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            nextQearyParam=request.form.get('next')
            #checked user exists
            user = User.query.filter_by(email=email).first()
            
            if  user :
                if check_password_hash(user.password,password):
                    login_user(user)
                    return redirect(nextQearyParam or url_for('panel'))
                else:
                    flash("wrong password")
                    return redirect(url_for('login'))
            else:
                flash('wrong in form')
                return redirect(url_for('login'))
           
    return render_template('login.html', form=form)
@app.route('/logout',methods=['post'])
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

@app.route('/panel/editprofile')
@login_required
def EditProfile():
    return 'Edit Profile page'


# تنظیم مسیر ذخیره‌سازی تصاویر
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/panel/upload', methods=['GET','POST'])
@login_required
def uploadAvatar():
    if request.method == 'POST':
        # بررسی اینکه آیا فایل در درخواست وجود دارد
        if 'pic' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['pic']
        
        # اگر کاربر فایلی انتخاب نکرده باشد
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # اگر فایل مجاز باشد
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = Image.open(file)
            
            # تغییر اندازه تصویر به 150x150 پیکسل
            img = img.resize((100, 100))
            
            # ذخیره تصویر با اندازه جدید
            img.save(file_path)
            
            
            
            # به‌روزرسانی مسیر آواتار کاربر در دیتابیس
            current_user.avatar = f'/img/{filename}'
            db.session.commit()
            
            flash('Avatar updated successfully!')
            return redirect(url_for('panel'))
    
    return render_template('Avatar.html')
                              
with app.app_context():
 db.create_all()
 print('Database connection established....')




if __name__ == '__main__':
    app.run(debug=True)