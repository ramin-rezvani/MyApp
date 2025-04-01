from flask import Blueprint
from controller.admin import AdminController

bp = Blueprint('admin', __name__, url_prefix='/admin')
admin = AdminController()

bp.add_url_rule('', 'index', admin.index, methods=['GET'])
bp.add_url_rule('/info', 'AdminInformation', admin.AdminInformation, methods=['GET'])
bp.add_url_rule('/changepassword', 'AdminChangePassword', admin.AdminChangePassword, methods=['GET', 'POST'])
bp.add_url_rule('/editprofile', 'AdminEditProfile', admin.AdminEditProfile, methods=['GET', 'POST'])
bp.add_url_rule('/upload', 'AdminUploadAvatar', admin.AdminUploadAvatar, methods=['GET', 'POST'])
bp.add_url_rule('/newuser', 'AddNewUser', admin.AddNewUser, methods=['GET', 'POST'])
bp.add_url_rule('/user', 'GetUserList', admin.GetUserList, methods=['GET', 'POST'])
bp.add_url_rule('/course/new', 'AddNewCourse', admin.AddNewCourse, methods=['GET', 'POST'])
bp.add_url_rule('/course', 'GetCourseList', admin.GetCourseList, methods=['GET', 'POST'])
bp.add_url_rule('/course/edit/<int:course_id>', 'EditCourse', admin.EditCourse, methods=['GET', 'POST'])
bp.add_url_rule('/episode/edit', 'EditEpisode', admin.EditEpisode, methods=['GET', 'POST'])
bp.add_url_rule('/episode/new', 'AddNewEpisode', admin.AddNewEpisode, methods=['GET', 'POST'])
bp.add_url_rule('/episode', 'GetEpisode', admin.GetEpisode, methods=['GET', 'POST'])
bp.add_url_rule('/category/new', 'AddNewCategory', admin.AddNewCategory, methods=['GET', 'POST'])
bp.add_url_rule('/category', 'GetCategoryList', admin.GetCategoryList, methods=['GET', 'POST'])
bp.add_url_rule('/category/edit', 'EditCategory', admin.EditCategory, methods=['GET', 'POST'])
bp.add_url_rule('/comments', 'GetCommentList', admin.GetCommentList, methods=['GET', 'POST'])
bp.add_url_rule('/comments/approve', 'ApproveComment', admin.ApproveComment, methods=['POST'])