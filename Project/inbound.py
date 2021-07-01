from flask import Blueprint, render_template, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import User, Providers, SKU, BuyOrder
from . import db
from datetime import datetime
inbound = Blueprint('inbound', __name__)

# Nueva orden
@inbound.route('/new_order')
@login_required
def new_order():
    userID = User.get_id(current_user)
    providers_list = []
    for provider in Providers.query.filter_by(userID=userID).all():
        providers_list.append(provider.name)
    SKU_list = {}
    for sku in SKU.query.filter_by(userID=userID).all():
        SKU_list[sku.SKUID] = sku.description
    return render_template("logged/inbound/new_order.html", name=current_user.name, SKU_list=SKU_list, provider_list=providers_list)

# Nuevo producto
@inbound.route('/new_product')
@login_required
def new_product():
    return render_template("logged/inbound/new_product.html", name=current_user.name)

# Nuevo proveedor
@inbound.route('/new_provider')
@login_required
def new_provider():
    return render_template("logged/inbound/new_provider.html", name=current_user.name)



@inbound.route('/new_order', methods=["POST"])
@login_required
def post_new_order():


    userID = User.get_id(current_user) # Obtengo el userID del usuario actual
    date = datetime.strptime(request.form.get("date"), "%Y-%m-%d") # Obtengo el date
    provider = request.form.get("providers") # Obtengo el proveedor del formulario
    IDBuy = request.form.get("IDBuy") # Obtengo el ID de compra del formulario
    IDReceipt = request.form.get("IDReceipt") # Obtengo el ID de recepción del formulario
    ID = len(BuyOrder.query.all()) + 1 # Obtengo el nuevo ID para la nueva row
    IDOrder = len(BuyOrder.query.filter_by(userID=userID).all()) + 1 # Obtengo la ID de compra 

    dict_form = request.form.to_dict() # Convierto la información del formulario en diccionario
    del dict_form["date"] # Elimino todos los campos que no son con respecto a los SKU
    del dict_form["providers"]
    del dict_form["IDBuy"]
    del dict_form["IDReceipt"]

    SKUs = {}  # Creo el diccionario donde se va a almacenar la información de los skus obtenidos por el formulario
    for key, val in dict_form.items():
        position = ""
        if "auto" in key:
            position = key[4:]
            key = key[:4]
        elif "SKU" in key:
            position = key[3:]
            key = key[:3]

        elif "description" in key:
            position = key[11:]
            key = key[:11]

        elif "quantity" in key:
            position = key[8:]
            key = key[:8]

        if position not in SKUs:
            SKUs[position] = {key : val}
        else:
            SKUs[position][key] = val
    
    # Obtengo el ID del proveedor 
    IDProvider = Providers.query.filter_by(userID=userID, name=provider).first().IDProvider 
    
    if not IDProvider: # En caso de que no haya proveedor, creo uno
        IDProvider = Providers.insert_for_id(userID, provider) # Creo una nueva entry para el usuario especificado

    # Obtengo los SKUs y en caso de que no estén, los sumo a la base de datos
    for key in SKUs:

        if "SKU" not in SKUs[key]: # Quiere decir que el EAN|SKU es automático
            description = SKUs[key]["description"]
            IDObj = SKU.query.filter_by(userID=userID, description=description).first()
            if not IDObj: # En caso de que no exista la descripción...
                SKUs[key]["SKU"] = SKU.create_sku(SKU, userID, description) # Creo un SKU con la descripción y se lo asigno al json
            else:
                SKUs[key]["SKU"] = IDObj.SKUID
                del SKUs[key]["auto"] # Elimino la key

        else: # En caso de que el SKU haya sido ingresado manualmente
            SKUID = SKUs[key]["SKU"]
            description = SKUs[key]["description"]
            if not SKU.query.filter_by(userID=userID, SKUID=SKUID).first(): # En caso de que no exista el SKU
                SKU.create_product(SKU, userID, SKUID, description)


    if not IDBuy:
        data = BuyOrder(ID=ID, IDOrder=IDOrder, IDReceipt=IDReceipt, userID=userID, SKU=SKUs, IDProvider=IDProvider, date=date)
        db.session.add(data)
        db.session.commit()
    return redirect(url_for('inbound.new_order'))