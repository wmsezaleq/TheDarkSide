from flask import Flask
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "abcdefghijklmnñopqrstuvwxyz1234567890ABCDEFGHIJKNMLOPQRSTUVWXYZslipKnot!2123#"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Deshabilito la función deprecada para debug

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Template para las rutas de auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Template para las que no sean de auth
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app