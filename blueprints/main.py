from flask import Blueprint
from controller.home import HomeController

bp = Blueprint('main', __name__)
home = HomeController()

bp.add_url_rule('/', 'Main', home.Main)
bp.add_url_rule('/search', 'getResultSearch', home.getResultSearch)
bp.add_url_rule('/deleteCourse/<int:id>', 'DeleteCourse', home.DeleteCourse, methods=['POST'])
bp.add_url_rule('/addtobascket', 'AddToBascket', home.AddToBascket, methods=['GET', 'POST'])
bp.add_url_rule('/checkout', 'Checkout', home.Checkout, methods=['GET', 'POST'])
bp.add_url_rule('/Payment', 'Payment', home.Payment, methods=['GET', 'POST'])
bp.add_url_rule('/category/<string:name>', 'viewCategory', home.viewCategory)
bp.add_url_rule('/<string:slug>', 'Single', home.Single)
bp.add_url_rule('/<string:slug>/Comment', 'SendComment', home.SendComment, methods=['POST'])