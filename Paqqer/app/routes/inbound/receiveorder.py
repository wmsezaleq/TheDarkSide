from flask import Blueprint, render_template, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from app.models import User, Providers, SKU, BuyOrder, ReceiptOrder
from app import db
from datetime import datetime
receive_order = Blueprint('receive_order', __name__)

# Recepción de órdenes
@receive_order.route('/inbound/receive_order')
@login_required
def index():
    # userID = User.get_id(current_user)
    # providers_list = [] # Lista con los proveedores
    # SKU_list = {} # Diccionario con los SKU y su descripción

    # for provider in Providers.query.filter_by(userID=userID).all():
    #     providers_list.append(provider.name)
    # for sku in SKU.query.filter_by(userID=userID).all():
    #     SKU_list[sku.SKUID] = sku.description
    
    # return render_template("logged/inbound/receive_order.html", name=current_user.name, SKU_list=SKU_list, provider_list=providers_list)
    pass

@login_required
def post_index():
    # userID = User.get_id(current_user) # type: str
    # totalReceipt = ReceiptOrder.query.filter_by(userID=userID).count() #type: int
    # ReceiptOrder(
    #     IDReceipt=totalReceipt+1,
    #     userID=userID,
    #     date=datetime.now()
    # )
    pass