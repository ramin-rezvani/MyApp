from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import app, db  # وارد کردن app و db از extensions
from models import User
from forms import ChangePasswordForm, EditProfileForm
from werkzeug.utils import secure_filename
from PIL import Image
import os
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
uplode_dir= os.path.curdir + '/static/uploads/'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UserController:
    def __init__(self):
        self.register_routes()

    def register_routes(self):
        # تعریف مسیرها با استفاده از add_url_rule
        app.add_url_rule("/panel/info", "Information", self.Information, methods=['GET'])
        app.add_url_rule("/panel", "Panel", self.Panel, methods=['GET'])
        app.add_url_rule("/panel/changepassword", "ChangePassword", self.ChangePassword, methods=['GET', 'POST'])
        app.add_url_rule("/panel/editprofile", "EditProfile", self.EditProfile, methods=['GET', 'POST'])
        app.add_url_rule("/panel/upload", "UploadAvatar", self.UploadAvatar, methods=['GET', 'POST'])

    @login_required
    def Information(self):
        # نمایش اطلاعات کاربر
        return render_template('user/info.html', user=current_user)

    @login_required
    def Panel(self):
        # نمایش پنل کاربر
        return render_template('user/panel.html', user=current_user)

    @login_required
    def ChangePassword(self):
        form = ChangePasswordForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')
                
                # بررسی صحت رمز عبور قدیمی
                if check_password_hash(current_user.password, old_password):
                    # به‌روزرسانی رمز عبور جدید
                    current_user.password = generate_password_hash(new_password,method='pbkdf2:sha256')
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                    return redirect(url_for('Panel'))
                else:
                    flash('Old password is incorrect', 'error')
                    return redirect(url_for('ChangePassword'))
           
        return render_template('user/change_password.html', form=form)

    @login_required
    def EditProfile(self):
        form = EditProfileForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = request.form.get('name')
                
                email = request.form.get('email')
                
                # به‌روزرسانی اطلاعات کاربر
                current_user.name = name
                current_user.email = email
                db.session.commit()
                
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('Panel'))
           
        return render_template('user/edit_profile.html', form=form, user=current_user)
    
        # تنظیم مسیر ذخیره‌سازی تصاویر




    
    

    
    @login_required
    def UploadAvatar(self):
        if request.method == 'POST':
            # بررسی اینکه آیا فایل در درخواست وجود دارد
            if 'avatar' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            
            file = request.files['avatar']
            
            # اگر کاربر فایلی انتخاب نکرده باشد
            if file.filename == '':
                flash('No selected file', 'error')
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
                current_user.avatar = f'/uploads/{filename}'
                db.session.commit()
                
                flash('Avatar uploaded successfully!', 'success')
                return redirect(url_for('Panel'))
    
        return render_template('user/Avatar.html')