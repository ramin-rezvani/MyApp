from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import app, db  # وارد کردن app و db از extensions
from models import User,Course
from forms import ChangePasswordForm, EditProfileForm,NewUserForm,CourseForm
from werkzeug.utils import secure_filename
from PIL import Image
import os
from slugify import slugify

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
uplode_dir= os.path.curdir + '/static/uploads/'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class AdminController:
 def __init__(self):
    self.register_routes()
 def register_routes(self):
    # تعریف مسیرها با استفاده از add_url_rule
    app.add_url_rule("/admin", "index", self.index, methods=['GET'])
    app.add_url_rule("/admin/info", "AdminInformation", self.AdminInformation, methods=['GET'])
    #app.add_url_rule("/panel", "Panel", self.Panel, methods=['GET'])
    app.add_url_rule("/admin/changepassword", "AdminChangePassword", self.AdminChangePassword, methods=['GET', 'POST'])
    app.add_url_rule("/admin/editprofile", "AdminEditProfile", self.AdminEditProfile, methods=['GET', 'POST'])
    app.add_url_rule("/admin/upload", "AdminUploadAvatar", self.AdminUploadAvatar, methods=['GET', 'POST'])
    app.add_url_rule("/admin/newuser","AddNewUser",self.AddNewUser,methods=['GET','POST'])
    app.add_url_rule("/admin/course/new","AddNewCourse",self.AddNewCourse,methods=['GET','POST'])
    app.add_url_rule("/admin/course","GetCourseList",self.GetCourseList,methods=['GET','POST'])
 @login_required
 def AddNewUser(self):
    form = NewUserForm()
    if not current_user.admin:
     return redirect(url_for('panel'))
    if request.method == 'POST':
       if form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
        newUser =User(name=name,email=email,password = hashed_password )
        db.session.add(newUser)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('admin/NewUser.html',form=form)
 @login_required
 def index(self):
    if not current_user.admin:
        return redirect(url_for('panel'))
    return render_template('/admin/index.html')
 @login_required
 def AdminInformation(self):
    # نمایش اطلاعات کاربر
    return render_template('admin/info.html', user=current_user)

 @login_required
 def AdminChangePassword(self):
  if not current_user.admin:
   return redirect(url_for('panel'))
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
                   return redirect(url_for('index'))
               else:
                   flash('Old password is incorrect', 'error')
                   return redirect(url_for('AdminChangePassword'))
          
  return render_template('admin/change_password.html', form=form)
     
 @login_required
 def AdminEditProfile(self):
     if not current_user.admin:
       return redirect(url_for('panel'))
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
             return redirect(url_for('index'))
        
     return render_template('admin/edit_profile.html', form=form, user=current_user)
     
     # تنظیم مسیر ذخیره‌سازی تصاویر
     
     
     
 @login_required
 def AdminUploadAvatar(self):
     if not current_user.admin:
       return redirect(url_for('panel'))
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
             return redirect(url_for('index'))
     
     return render_template('admin/Avatar.html')
 
 @login_required
 def GetUserList(self):
  GetAllUser= User.query.all()
  if request.method == 'POST':
         print(request.args.get('id')) 
         db.session.query(User).filter_by(id= request.args.get('id')).delete()
         db.session.commit()
  GetAllUser= User.query.all()      
  return render_template('admin/userlist.html', users=GetAllUser)

 @login_required
 def AddNewCourse(self):
    form=CourseForm()
    if request.method == 'POST':
        if form.validate_on_submit() and 'pic' in request.files:
            title = request.form.get('title')
            content=request.form.get('content')
            price=request.form.get('price')
            picture=request.files['pic']       
            filename = picture.filename
                
            if not allowed_file(filename):
                flash('check pic','danger')
                return redirect(url_for('AddNewCourse'))
                
            filesecure = secure_filename(filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filesecure))
            
            newCourse=Course(title=title,content=content,price=price,user_id=current_user.id) 
            db.session.add(newCourse)
            db.session.commit()
            flash('new course created','success')
            return redirect(url_for('AddNewCourse'))
    return render_template('/admin/NewCourse.html',form=form)

 def GetCourseList(self):
     getall=Course.query.all()
     return render_template('/admin/courselist.html',courses=getall)



