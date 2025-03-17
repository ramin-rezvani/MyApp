from flask import render_template,request
from extensions import app
from models import User,Course
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
        course = Course.query.filter_by(slug=slug).one()
        return render_template('Single.html', course=course)

    