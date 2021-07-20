from flask import Blueprint, render_template, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from app.models import User, Providers, SKU, BuyOrder, ReceiptOrder
from app import db

abm_receiptorder = Blueprint('abm_receiptorder', __name__)



@abm_receiptorder.route('/abm/receiptorders/edit?<id>')
def edit(id):
    return id
