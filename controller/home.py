from flask import render_template,request,abort
from extensions import app
from models import User,Course,Episode
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
        episodes=Episode.query.filter_by(course_id=course.id).all()
        if not course:
          abort(404)  # یا یه صفحه 404 رندر کن
        return render_template('Single.html', course=course,episodes=episodes)   
        

    