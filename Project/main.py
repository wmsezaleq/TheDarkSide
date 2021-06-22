from .auth import login
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user:
        return render_template("logged/profile.html", name=current_user.name)
    else:
        return render_template("no-logged/index.html")

@main.route('/profile')
@login_required
def profile():
    return render_template("logged/profile.html", name=current_user.name)

@main.route('/test')
def test():
    return render_template("test.html")

