from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, Course, Episode, Category, Comment
from forms import ChangePasswordForm, EditProfileForm, NewUserForm, CourseForm, EpisodeForm, EditEpisodeForm, CategoryForm
from werkzeug.utils import secure_filename
from PIL import Image
import os
from slugify import slugify
import re
from unidecode import unidecode
from math import floor

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AdminController:
    @login_required
    def index(self):
        if not current_user.admin:
            return redirect(url_for('user.Panel'))
        return render_template('/admin/index.html')

    @login_required
    def AdminInformation(self):
        return render_template('admin/info.html', user=current_user)

    @login_required
    def AdminChangePassword(self):
        if not current_user.admin:
            return redirect(url_for('user.Panel'))
        form = ChangePasswordForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')
                if check_password_hash(current_user.password, old_password):
                    current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                    return redirect(url_for('admin.index'))
                else:
                    flash('Old password is incorrect', 'error')
                    return redirect(url_for('admin.AdminChangePassword'))
        return render_template('admin/change_password.html', form=form)

    @login_required
    def AdminEditProfile(self):
        if not current_user.admin:
            return redirect(url_for('user.Panel'))
        form = EditProfileForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                name = request.form.get('name')
                email = request.form.get('email')
                current_user.name = name
                current_user.email = email
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('admin.index'))
        return render_template('admin/edit_profile.html', form=form, user=current_user)

    @login_required
    def AdminUploadAvatar(self):
        if not current_user.admin:
            return redirect(url_for('user.Panel'))
        if request.method == 'POST':
            if 'avatar' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            file = request.files['avatar']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                img = Image.open(file)
                img = img.resize((100, 100))
                img.save(file_path)
                current_user.avatar = f'/uploads/{filename}'
                db.session.commit()
                flash('Avatar uploaded successfully!', 'success')
                return redirect(url_for('admin.index'))
        return render_template('admin/Avatar.html')

    @login_required
    def AddNewUser(self):
        form = NewUserForm()
        if not current_user.admin:
            return redirect(url_for('user.Panel'))
        if request.method == 'POST':
            if form.validate_on_submit():
                name = request.form.get('name')
                email = request.form.get('email')
                password = request.form.get('password')
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                newUser = User(name=name, email=email, password=hashed_password)
                db.session.add(newUser)
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('admin.index'))
        return render_template('admin/NewUser.html', form=form)
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
        form = CourseForm()
        categories = Category.query.all()
        if request.method == 'POST':
            if form.validate_on_submit() and 'pic' in request.files:
                title = request.form.get('title')
                content = request.form.get('content')
                price = request.form.get('price')
                category = request.form.get('category')
                picture = request.files['pic']
                filename = picture.filename
                if not allowed_file(filename):
                    flash('check pic', 'danger')
                    return redirect(url_for('admin.AddNewCourse'))
                filesecure = secure_filename(filename)
                file_path = os.path.join(UPLOAD_FOLDER, filesecure)
                picture.save(file_path)
                relative_path = f"uploads/{filesecure}"
                newCourse = Course(title=title, content=content, price=price,
                                 image=relative_path, user_id=current_user.id, category_id=category)
                db.session.add(newCourse)
                db.session.commit()
                flash('new course created', 'success')
                return redirect(url_for('admin.AddNewCourse'))
        return render_template('/admin/NewCourse.html', form=form, categories=categories)

    def GetCourseList(self):
        getall = Course.query.all()
        if request.method == 'POST':
            Course.query.filter_by(id=request.args.get('id')).delete()
            Episode.query.filter_by(course_id=request.args.get('id')).delete()
            db.session.commit()
            return redirect(url_for('admin.GetCourseList'))
        return render_template('/admin/courselist.html', courses=getall)

    def EditCourse(self, course_id):
        course = Course.query.get_or_404(course_id)
        form = CourseForm(obj=course)
        categories = Category.query.all()
        if request.method == 'POST' and form.validate_on_submit():
            course.title = form.title.data
            course.content = form.content.data
            course.price = form.price.data
            course.category_id = request.form.get('category')
            new_slug = slugify(form.title.data)
            existing_course = Course.query.filter_by(slug=new_slug).first()
            if existing_course and existing_course.id != course.id:
                new_slug = f"{new_slug}-{course.id}"
            course.slug = new_slug
            if 'pic' in request.files:
                picture = request.files['pic']
                if picture.filename:
                    filename = secure_filename(picture.filename)
                    if not allowed_file(filename):
                        flash('Invalid file type for picture.', 'danger')
                        return redirect(url_for('admin.EditCourse', course_id=course_id))
                    if course.image:
                        old_image_path = os.path.join(UPLOAD_FOLDER, course.image.split('/')[-1])
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    picture.save(file_path)
                    course.image = f"uploads/{filename}"
            db.session.commit()
            flash('Course updated successfully.', 'success')
            return redirect(url_for('admin.GetCourseList'))
        return render_template('/admin/EditCourse.html', form=form, course=course, categories=categories)

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
                newEpisode = Episode(title=title, body=content, number=number, course_id=course_id,
                                   videoUrl=videoUrl, time=time, type=typeCourse)
                db.session.add(newEpisode)
                db.session.commit()
                flash('Episode Created Successfully!', 'success')
                self.UpdateCourseTime(course_id)
                return redirect(url_for('admin.AddNewEpisode'))
        return render_template('/Admin/NewEpisode.html', form=form, courses=courses)

    def GetEpisode(self):
        if request.method == 'POST':
            courseId = request.form.get('courseid')
            Episode.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
            self.UpdateCourseTime(courseId)
            return redirect(url_for('admin.GetEpisode'))
        episodes = Episode.query.all()
        return render_template('/admin/EpisodeList.html', episodes=episodes)

    def EditEpisode(self):
        form = EditEpisodeForm()
        episode = Episode.query.filter_by(id=request.args.get('id')).first()
        courses = Course.query.all()
        if request.method == 'POST':
            if form.validate_on_submit() and request.form.get('body') != '':
                title = request.form.get('title')
                content = request.form.get('body')
                number = request.form.get('number')
                course_id = request.form.get('course')
                videoUrl = request.form.get('videoUrl')
                time = request.form.get('time')
                typeCourse = request.form.get('type')
                episode.title = title
                episode.body = content
                episode.number = number
                episode.course_id = course_id
                episode.videoUrl = videoUrl
                episode.time = time
                episode.type = typeCourse
                db.session.add(episode)
                db.session.commit()
                self.UpdateCourseTime(course_id)
                return redirect(url_for('admin.GetEpisode'))
        return render_template('/admin/EditEpisode.html', form=form, episode=episode, courses=courses)

    def AddNewCategory(self):
        if not current_user.admin:
            abort(403)
        form = CategoryForm()
        if form.validate_on_submit():
            new_category = Category(name=form.name.data)
            db.session.add(new_category)
            db.session.commit()
            flash('Category Created Successfully', 'success')
            return redirect(url_for('admin.AddNewCategory'))
        categories = Category.query.all()
        return render_template('/admin/Categories/NewCategory.html', form=form)

    def GetCategoryList(self):
        if request.method == 'POST':
            Category.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
            return redirect(url_for('admin.GetCategoryList'))
        categories = Category.query.all()
        return render_template('admin/Categories/ListCategory.html', categories=categories)

    def EditCategory(self):
        if not current_user.admin:
            abort(403)
        category_id = request.args.get('id') if request.method == 'GET' else request.form.get('category_id')
        if not category_id:
            flash('Category ID is missing.', 'danger')
            return redirect(url_for('admin.GetCategoryList'))
        try:
            category_id = int(category_id)
        except (ValueError, TypeError):
            flash('Invalid category ID.', 'danger')
            return redirect(url_for('admin.GetCategoryList'))
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            flash('Category not found.', 'danger')
            return redirect(url_for('admin.GetCategoryList'))
        form = CategoryForm(obj=category)
        if form.validate_on_submit():
            category.name = form.name.data
            db.session.commit()
            flash('Category updated successfully!', 'success')
            return redirect(url_for('admin.GetCategoryList'))
        return render_template('/admin/Categories/EditCategory.html', form=form, category=category)

    def UpdateCourseTime(self, courseId):
        course = Course.query.filter_by(id=courseId).one()
        episodes = Episode.query.filter_by(course_id=courseId).all()
        course.time = self.UpdateTime(episodes)
        db.session.add(course)
        db.session.commit()

    def UpdateTime(self, episodes):
        second = 0
        for episode in episodes:
            time = episode.time.split(':')
            if len(time) == 2:
                second += int(time[0]) * 60
                second += int(time[1])
            if len(time) == 3:
                second += int(time[0]) * 3600
                second += int(time[1]) * 60
                second += int(time[2])
        minutes = floor(second / 60)
        hours = floor(minutes / 60)
        second = floor(((second / 60) % 1) * 60)
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, second)

    @login_required
    def GetCommentList(self):
        if request.method == 'POST':
            Comment.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
            comments = Comment.query.all()
            return render_template('admin/CommentList.html', comments=comments)
        return render_template('admin/CommentList.html', comments=Comment.query.all())

    @login_required
    def ApproveComment(self):
        comment = Comment.query.filter_by(id=request.args.get('id')).one()
        comment.status = True
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('admin.GetCommentList'))