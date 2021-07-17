from flask import Blueprint, render_template, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from ..models import User, Providers, SKU, BuyOrder, ReceiptOrder
from .. import db
from datetime import datetime
abm = Blueprint('abm', __name__)

# Recepción de órdenes
@abm.route('/new_buyorder')
@login_required
def new_buyorder():
    userID = User.get_id(current_user)
    providers_list = [] # Lista con los proveedores
    SKU_list = {} # Diccionario con los SKU y su descripción

    for provider in Providers.query.filter_by(userID=userID).all():
        providers_list.append(provider.name)
    for sku in SKU.query.filter_by(userID=userID).all():
        SKU_list[sku.SKUID] = {
            "Descripcion" : sku.description,
            "Precio" : sku.price,
            }
    
    return render_template("logged/abm/new_buyorder.html", name=current_user.name, SKU_list=SKU_list, provider_list=providers_list)

@abm.route('/new_buyorder', methods=["POST"])
@login_required
def post_new_buyorder():
    userID = User.get_id(current_user) # type: str
    totalReceipt = ReceiptOrder.query.filter_by(userID=userID).count() #type: int
    ReceiptOrder(
        IDReceipt=totalReceipt+1,
        userID=userID,
        date=datetime.now()
    )