from flask import render_template
from extensions import app
class HomeController:
    def __init__(self):
        self.app = app
        self.register_routes()

    def register_routes(self):
        # تعریف مسیر '/' با استفاده از add_url_rule
        self.app.add_url_rule('/', 'main', self.Main)

    def Main(self):
        return render_template('home.html')