from flask import Flask
from flask_login.login_manager import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autoflush":False})
io = SocketIO()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "abcdefghijklmnñopqrstuvwxyz1234567890ABCDEFGHIJKNMLOPQRSTUVWXYZslipKnot!2123#"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Deshabilito la función deprecada para debug

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    io.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Template para las rutas de auth
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Template para las que no sean de auth
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routes.inbound import inbound as inbound_blueprint
    app.register_blueprint(inbound_blueprint)

    from .routes.abm.buyorders import abm_buyorder as abm_buyorders_blueprint
    app.register_blueprint(abm_buyorders_blueprint)

    from .routes.abm.receiptorders import abm_receiptorder as abm_receiptorders_blueprint
    app.register_blueprint(abm_receiptorders_blueprint)

    from .ioRoutes import abm as abm_ioblueprint

    return app