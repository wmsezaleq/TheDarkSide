from ..auth import login
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .. import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    try:
        if current_user.name:
            return redirect(url_for("main.dashboard"))
    except:
        pass
    return render_template("no-logged/index.html")

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template("logged/dashboard.html", name=current_user.name)

@main.route('/profile')
@login_required
def profile():
    return render_template("logged/profile.html", name=current_user.name)

@main.route('/test')
def test():
    return render_template("test.html")

