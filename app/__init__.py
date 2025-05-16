from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_login import login_required, current_user, UserMixin, logout_user, login_user
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os

load_dotenv()

db = SQLAlchemy()

migrate = Migrate()

def create_app(testing=False):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        app.config['WTF_CSRF_ENABLED'] = False  

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    csrf = CSRFProtect()
    csrf.init_app(app)

    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    from .routes import auth_bp
    app.register_blueprint(auth_bp)


    with app.app_context():
        from . import models
        db.create_all()

    return app
