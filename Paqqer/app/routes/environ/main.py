from app.auth import login
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db

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
    return render_template("logged/environ/dashboard.html", name=current_user.name)

@main.route('/profile')
@login_required
def profile():
    return render_template("logged/environ/profile.html", name=current_user.name)

@main.route('/test', methods=["GET"])
def test():
    print(request.args)
    return ""