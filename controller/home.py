from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import User, Course, Episode, Category, Bascket, Comment

class HomeController:
    def Main(self):
        page = request.args.get('page', default=1, type=int)
        allCourses = Course.query.paginate(page=page, per_page=2)
        return render_template('Home.html', courses=allCourses)

    def Single(self, slug):
        course = Course.query.filter_by(slug=slug).first()
        episodes = Episode.query.filter_by(course_id=course.id).all()
        comments = Comment.query.filter_by(course_id=course.id, status=True).all()
        return render_template('Single.html', course=course, episodes=episodes, comments=comments)

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
        courseId = request.form.get('course_id')
        slug = request.form.get('slug')
        user_id = current_user.id
        BascketQuery = Bascket.query.filter_by(user_id=user_id).all()
        if BascketQuery:
            for product in BascketQuery:
                if product.course_id == courseId:
                    flash('Course Was Added To Bascket')
                    return redirect(url_for('main.Single', slug=slug))
        newBascket = Bascket(user_id=user_id, course_id=courseId)
        db.session.add(newBascket)
        db.session.commit()
        return redirect(url_for('main.Checkout'))

    def Checkout(self):
        basckets = Bascket.query.filter_by(user_id=current_user.id).all()
        total_price = 0
        for product in basckets:
            total_price += int(product.GetCourse().price)
        return render_template('Checkout.html', bascket=basckets, total_price=total_price)

    def DeleteCourse(self, id):
        Bascket.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('main.Checkout'))

    def Payment(self):
        baskets = Bascket.query.filter_by(user_id=current_user.id).all()
        total_price = 0
        listId = []
        for product in baskets:
            total_price += int(product.GetCourse().price)
            listId.append(str(product.GetCourse().id))
        # Payment OK --- CallBackPayment --- SUCCESSFULL
        for item in listId:
            items = Course.query.filter_by(id=int(item)).first()
            items.students = ",".join(str(items.students) + "," + ",".join(str(current_user.id)))
            db.session.add(items)
            db.session.commit()
        Bascket.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return redirect(url_for('main.Main'))

    def SendComment(self, slug):
        user_id = current_user.id
        course = Course.query.filter_by(slug=slug).first()
        text = request.form.get('text')
        newComment = Comment(user_id=user_id, course_id=course.id, text=text)
        db.session.add(newComment)
        db.session.commit()
        return redirect(url_for('main.Single', slug=slug))