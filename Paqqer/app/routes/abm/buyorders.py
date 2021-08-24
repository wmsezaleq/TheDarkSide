from sqlalchemy.orm import query
from sqlalchemy.sql.functions import user
from app.auth import login
from flask import Blueprint, render_template, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from app.models import User, Providers, SKU, BuyOrder, ReceiptOrder
from app import db
from datetime import datetime, timedelta
import json

abm_buyorder = Blueprint('abm_buyorder', __name__)


# Recepción de órdenes

@abm_buyorder.route('/abm/buyorders/index')
@login_required
def index():
    '''
    En el index del ABM voy a mostrar todas las órdenes de
    retiro para poder seleccionar una por una y modificarlas a gusto
    '''
    userID = User.get_id(current_user)
    ayer = datetime.date(datetime.now() - timedelta(1))
    semana_que_viene = datetime.date(datetime.now() + timedelta(7))
    orders = BuyOrder.getDict(BuyOrder, 
                             data=BuyOrder.query.filter_by(userID=userID), 
                             fromDate=ayer, 
                             toDate=semana_que_viene)
    return render_template("logged/abm/buyorder/index.html", 
                            name=current_user.name,
                            userID = userID,
                            orders=orders, 
                            fromDate=ayer.strftime("%Y-%m-%d"),
                            toDate=semana_que_viene.strftime("%Y-%m-%d"))

@abm_buyorder.route('/abm/buyorders/new')
@login_required
def new():
    userID = User.get_id(current_user)
    providers_list, queryProviders = Providers.getNameList(Providers, userID)

    SKU_list = SKU.getDict(SKU, SKU.query.filter_by(userID=userID).all()) # type: dict
    return render_template("logged/abm/buyorder/new.html", name=current_user.name, userID=userID, SKU_list=SKU_list, providers_list=providers_list, queryProviders=queryProviders)

from datetime import datetime

@abm_buyorder.route('/abm/buyorders/new', methods=["POST"])
@login_required
def post_new():
    userID = User.get_id(current_user) # type: str
    totalOrders = BuyOrder.query.filter_by(userID=userID).count()

    date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
    providerName = request.form.get("providers")
    providerID = Providers.query.filter_by(userID=userID, name=providerName).first().IDProvider


    i = 0
    productos = {}
    while True:
        SKUID = request.form.get(f"SKU{i}")
        if SKUID == None:
            break
        quantity = request.form.get(f"quantity{i}")
        price = request.form.get(f"price{i}")

        productos[SKUID] = {"quantity" : quantity, "price" : price}
        i += 1
    
    ordenRecepcion = ReceiptOrder(
        IDReceipt=ReceiptOrder.query.filter_by(userID=userID).count(),
        userID=userID,
        date=date
    )
    IDBuyOrder = BuyOrder.query.filter_by(userID=userID).count()
    buyorder = BuyOrder(
        IDOrder=IDBuyOrder,
        IDReceipt=ordenRecepcion.IDReceipt,
        userID=userID,
        SKU=productos,
        IDProvider=providerID,
        date=date
    )

    db.session.add(ordenRecepcion)
    db.session.add(buyorder)
    db.session.commit()

    return redirect(url_for('abm_buyorder.good', 
                            IDBuyOrder=IDBuyOrder, 
                            IDReceiptOrder=ordenRecepcion.IDReceipt))

@abm_buyorder.route('/abm/buyorders/good?IDReceiptOrder=<IDReceiptOrder>&IDBuyOrder=<IDBuyOrder>')
@login_required
def good(IDReceiptOrder, IDBuyOrder):
    return render_template('logged/abm/buyorder/good.html', name=current_user.name, IDBuyOrder=IDBuyOrder, IDReceiptOrder=IDReceiptOrder)

@abm_buyorder.route('/abm/buyorders/edit?<id>', methods=["GET"])
@login_required
def edit(id):
    userID = User.get_id(current_user)
    order = BuyOrder.query.filter_by(userID=userID, IDOrder=id).first()
    
    data = {
        "date" : order.date.strftime("%Y-%m-%d"),
        "IDOrder" : order.IDOrder,
        "IDReceipt" : order.IDReceipt,
        "SKU" : order.SKU,
        "Provider" : Providers.query.filter_by(userID=userID, IDProvider=order.IDProvider).first().name,
    }

    SKU_list = SKU.getDict(SKU, SKU.query.filter_by(userID=userID).all())
    providers_list, queryProviders = Providers.getNameList(Providers, userID)

    return render_template('logged/abm/buyorder/edit.html', userID=userID,
                                                            name=current_user.name,
                                                            data=data, 
                                                            SKU_list=SKU_list, 
                                                            provider_list=providers_list,
                                                            queryProviders=queryProviders)


@abm_buyorder.route('/abm/buyorders/edit?<id>POST', methods=["POST"])
@login_required
def post_edit(id):
    userID = User.get_id(current_user)
    date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
    providerName = request.form.get("providers")
    providerID = Providers.query.filter_by(userID=userID, name=providerName).first().IDProvider


    i = 0
    productos = {}
    while True:
        SKUID = request.form.get(f"SKU{i}")
        if SKUID == None:
            break
        quantity = request.form.get(f"quantity{i}")
        price = request.form.get(f"price{i}")

        productos[SKUID] = {"quantity" : quantity, "price" : price}
        i += 1

    bOrder = BuyOrder.query.filter_by(userID=userID, IDOrder=id).first()
    bOrder.SKU = productos
    bOrder.IDProvider = providerID
    bOrder.date = date
    db.session.commit()
    return redirect(url_for('abm_buyorder.good', 
                            IDBuyOrder=id, 
                            IDReceiptOrder=bOrder.IDReceipt))
