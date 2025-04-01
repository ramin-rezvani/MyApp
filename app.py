from flask import Flask
from extensions import db, loginmanager
import secrets
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)
    
    # Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'shop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeTG-4qAAAAAFeKMuo0SJHrXkJepmHtLD5MqFvi'
    app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeTG-4qAAAAAAcnjWJqkTgmygBE74rPH3LW94OY'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    # Initialize extensions
    db.init_app(app)
    loginmanager.init_app(app)
    
    # Register blueprints
    from blueprints.main import bp as main_bp
    from blueprints.auth import bp as auth_bp
    from blueprints.user import bp as user_bp
    from blueprints.admin import bp as admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    # Template filter
    @app.template_filter('Commafy')
    def commafy(value):
        try:
            if isinstance(value, str):
                value = ''.join(filter(str.isdigit, value))
            value = int(value)
            return "{:,}".format(value)
        except (ValueError, TypeError):
            return value

    # Context processor
    from models import Category
    @app.context_processor
    def context_processor():
        return {'categories': Category.query.all()}

    with app.app_context():
        db.create_all()
        print('Database connection established....')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)