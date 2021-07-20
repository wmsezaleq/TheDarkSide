from flask import Blueprint, render_template, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from ..models import User, Providers, SKU, BuyOrder, ReceiptOrder
from .. import db
from datetime import datetime
inbound = Blueprint('inbound', __name__)

# Recepción de órdenes
@inbound.route('/receive_order')
@login_required
def receive_order():
    userID = User.get_id(current_user)
    providers_list = [] # Lista con los proveedores
    SKU_list = {} # Diccionario con los SKU y su descripción

    for provider in Providers.query.filter_by(userID=userID).all():
        providers_list.append(provider.name)
    for sku in SKU.query.filter_by(userID=userID).all():
        SKU_list[sku.SKUID] = sku.description
    
    return render_template("logged/inbound/receive_order.html", name=current_user.name, SKU_list=SKU_list, provider_list=providers_list)

@inbound.route('/put_away')
@login_required
def put_away():
    return render_template("logged/inbound/put_away.html", name=current_user)

@inbound.route('/receive_order', methods=["POST"])
@login_required
def post_receive_order():
    userID = User.get_id(current_user) # type: str
    totalReceipt = ReceiptOrder.query.filter_by(userID=userID).count() #type: int
    ReceiptOrder(
        IDReceipt=totalReceipt+1,
        userID=userID,
        date=datetime.now()
    )