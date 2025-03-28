from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import app, db  # وارد کردن app و db از extensions
from models import User,Course,Episode,Category,Bascket
from forms import ChangePasswordForm, EditProfileForm,NewUserForm,CourseForm,EpisodeForm,EditEpisodeForm,CategoryForm
from werkzeug.utils import secure_filename
from PIL import Image
import os
from slugify import slugify
import re
from unidecode import unidecode
from math import floor

class HomeController:
    def __init__(self):
        self.app = app
        self.register_routes()

    def register_routes(self):
        # تعریف مسیر '/' با استفاده از add_url_rule
        self.app.add_url_rule('/', 'main', self.Main)
    def Main(self):
        page = request.args.get('page', default=1, type=int)
        allCourses = Course.query.paginate(page=page, per_page=2)
        return render_template('Home.html', courses=allCourses)

    def Single(self, slug):
        course = Course.query.filter_by(slug=slug).first()
        if not course:
          abort(404)  # یا یه صفحه 404 رندر کن
        episodes=Episode.query.filter_by(course_id=course.id).all()
        return render_template('Single.html', course=course,episodes=episodes)   
        
    def viewCategory(self, name):
     getCategory = Category.query.filter_by(name=name).first()
     if not getCategory:
          abort(404)
     page = request.args.get('page', default=1, type=int)
     getCourses = Course.query.filter_by(category_id=getCategory.id).paginate(page=page, per_page=3)
     return render_template('Category.html', courses=getCourses, category=getCategory) 
  
    def getResultSearch(self):
     list_posts = []
     searchInput = request.args.get('s')
     posts = Course.query.all()
    
     for post in posts:
        if searchInput.lower() in post.title.lower() or searchInput.lower() in post.content.lower():
          list_posts.append(post)
    
     return render_template('resultSearch.html', searchInput=searchInput, courses=list_posts)   
 
    def AddToBascket(self):
        courseId=request.form.get('course_id')
        slug= request.form.get('slug')
        user_id = current_user.id
        BascketQuery = Bascket.query.filter_by(user_id=user_id).all()
        if BascketQuery:
            for product in BascketQuery:
                if product.course_id == courseId:
                    flash('Course Was Added To Bascket')
                    return redirect(url_for('Single', slug=slug))
        
        newBascket = Bascket(user_id=user_id, course_id=courseId)
        db.session.add(newBascket)
        db.session.commit()
        return redirect(url_for('Checkout'))

    def Checkout(self):
        basckets = Bascket.query.filter_by(user_id=current_user.id).all()
        total_price= 0
        for product in basckets:
            total_price += int(product.GetCourse().price)
        return render_template('Checkout.html', bascket=basckets,total_price=total_price)

    def DeleteCourse(self, id):
        Bascket.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('Checkout'))
        

    