from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import app, db  # وارد کردن app و db از extensions
from models import User,Course,Episode
from forms import ChangePasswordForm, EditProfileForm,NewUserForm,CourseForm,EpisodeForm
from werkzeug.utils import secure_filename
from PIL import Image
import os
from slugify import slugify
import re
from unidecode import unidecode


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
    app.add_url_rule("/admin/course/edit/<int:course_id>'","EditCourse",self.EditCourse,methods=['Get','POST'])
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
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filesecure)
            picture.save(file_path)  
            # مسیر نسبی برای دیتابیس
            relative_path = f"uploads/{filesecure}"  
          
            
            newCourse=Course(title=title,content=content,price=price,image=relative_path,user_id=current_user.id) 
            db.session.add(newCourse)
            db.session.commit()
            flash('new course created','success')
            return redirect(url_for('AddNewCourse'))
    return render_template('/admin/NewCourse.html',form=form)

 def GetCourseList(self):
     getall=Course.query.all()
     if request.method=='POST':
         Course.query.filter_by(id=request.args.get('id')).delete()
         db.session.commit()
         return redirect(url_for('GetCourseList'))
     return render_template('/admin/courselist.html',courses=getall)
 
 def slugify(text):
    text = unidecode(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    text = text.strip('-')
    return text

 

 def EditCourse(self,course_id):
    # دریافت دوره موجود برای ویرایش
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)  # پر کردن فرم با داده‌های موجود

    if request.method == 'POST' and form.validate_on_submit():
        # به‌روزرسانی داده‌های دوره
        course.title = form.title.data
        course.content = form.content.data
        course.price = request.form.get('price')
        new_slug = slugify(form.title.data)

        # بررسی منحصربه‌فرد بودن slug
        existing_course = Course.query.filter_by(slug=new_slug).first()
        if existing_course and existing_course.id != course.id:
            new_slug = f"{new_slug}-{course.id}"  # اضافه کردن id برای منحصربه‌فرد بودن
        course.slug = new_slug

        # مدیریت تصویر
        if 'pic' in request.files:
            picture = request.files['pic']
            if picture.filename:  # اگر تصویر جدید آپلود شده است
                filename = secure_filename(picture.filename)
                if not allowed_file(filename):
                    flash('Invalid file type for picture.', 'danger')
                    return redirect(url_for('EditCourse', course_id=course_id))

                # حذف تصویر قدیمی (اگر وجود دارد)
                if course.image:
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], course.image.split('/')[-1])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                # ذخیره تصویر جدید
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                picture.save(file_path)
                course.image = f"uploads/{filename}"  # مسیر نسبی برای دیتابیس

        db.session.commit()
        flash('Course updated successfully.', 'success')
        return redirect(url_for('GetCourseList'))

    return render_template('/admin/EditCourse.html', form=form, course=course)

 @login_required
 def AddNewEpisode(self):
  form = EpisodeForm()
  courses = Course.query.all()
  if request.method == 'POST':
            if form.validate_on_submit():
                title = request.form.get('title')
                content = request.form.get('content')
                number = request.form.get('number')
                course_id = request.form.get('course')
                videoUrl = request.form.get('videoUrl')
                time = request.form.get('time')
                typeCourse = request.form.get('type')

                newEpisode = Episode(
                    title=title,
                    body=content,
                    number=number,
                    course_id=course_id,
                    videoUrl=videoUrl,
                    time=time,
                    type=typeCourse
                )
                db.session.add(newEpisode)
                db.session.commit()
                flash('Episode Created Successfully!', 'success')
                return redirect(url_for('AddNewEpisode'))
  return render_template('/Admin/NewEpisode.html', form=form, courses=courses)
 
 def GetEpisode(self):
      if request.method=='POST':
          Episode.query.filter_by(id=request.args.get('id')).delete()
          db.session.commit()
          return redirect(url_for('GetEpisode'))
      episodes=Episode.query.all()
      return render_template('/admin/EpisodeList.html',episodes=episodes)
  
 def EditEpisode(self,course_id):
      pass