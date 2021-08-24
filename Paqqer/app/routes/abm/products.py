from flask import Blueprint, request, Response
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import current_user, login_required
from sqlalchemy import cast, Integer
from werkzeug.utils import redirect, secure_filename
from app import db
from app.models import SKU, User, IMG
import base64
abm_products = Blueprint("abm_products", __name__)

@abm_products.route("/abm/products", methods=["GET", "POST"])
@login_required
def index():
    userID = User.get_id(current_user)
    text = request.form.get("search")
    data = None
    if text:
        type = request.form.get("type")
        SKUparam = None
        if type == "description":
            SKUparam = SKU.description
        else:
            SKUparam = SKU.SKUID
        data = SKU.getDict(SKU, SKU.query.filter(SKU.userID==userID, 
                                                SKUparam.contains(text))
                                                .order_by(SKU.INTSKU.asc())
                                                .all()) # Obtengo el diccionario de los SKU en esta página
    else:
        data = SKU.getDict(SKU, SKU.query.filter_by(userID=userID).order_by(SKU.INTSKU.asc()).all()) # Obtengo el diccionario de los SKU en esta página
    for key in data:
        '''
        Ciclo todas las key (que son los SKUID) estableciéndole l
        a imagen desde la base de datos de las imagenes
        Les agrego el tipo de formato (mimetype) y el formato codificado en base64 para
        después decodificarlo en la parte del usuario en el front-end
        '''
        try:
            img = IMG.query.filter_by(userID=userID, SKU=key).first()
            data[key]["Foto"]["mimetype"] = img.mimetype
            data[key]["Foto"]["img"] = img.img

        except Exception as e:
            continue
    return render_template("logged/abm/SKU/index.html", name=current_user.name, 
                                                        data=data, 
                                                        userID=userID)

@abm_products.route('/abm/products/newproduct', methods=["POST"])
@login_required
def post_product():
    userID = User.get_id(current_user)
    # Creación del SKU
    INTSKU = SKU.query.filter_by(userID=userID).order_by(SKU.SKUID.desc()).first().ID + 1
    SKUID=SKU.getSKU(SKU, INTSKU)
    sku_obj = SKU(
        SKUID = SKUID,
        INTSKU=INTSKU,
        userID=userID,
        description = request.form.get("descripcion"),
        price= float(request.form.get("precio"))
    )
    db.session.add(sku_obj)


    image = request.files["img"]
    if image:
        filename = secure_filename(image.filename) # Obtengo el nombre del archivo
        mimetype = image.mimetype # Obtengo el tipo de imagen
        imagen = IMG(
            userID=userID,
            img=base64.b64encode(image.read()),
            mimetype=mimetype,
            name=filename,
            SKU=SKUID
        ) # Creo el objeto imagen codificando en b64 la información en bin de la imagen
        db.session.add(imagen)
    db.session.commit()
    
    return redirect(url_for('abm_products.index'))


@abm_products.route('/abm/products/edit', methods=["POST"])
@login_required
def post_editproduct():
    userID = User.get_id(current_user)
    # Creación del SKU
    SKUID=request.form.get('SKUID')
    skuObj = SKU.query.filter_by(userID=userID, SKUID=SKUID).first() # type: SKU
    skuObj.description = request.form.get('descripcion')
    skuObj.price = float(request.form.get('precio'))


    image = request.files["img"]
    if image:
        filename = secure_filename(image.filename) # Obtengo el nombre del archivo
        mimetype = image.mimetype # Obtengo el tipo de imagen
        try:
            IMG.query.filter_by(userID=userID, SKU=SKUID).delete() # Elimino la vieja imagen si es que existe
        except:
            pass
        
        imagen = IMG(
            userID=userID,
            img=base64.b64encode(image.read()),
            mimetype=mimetype,
            name=filename,
            SKU=SKUID
        ) # Creo el objeto imagen codificando en b64 la información en bin de la imagen
        db.session.add(imagen)
    db.session.commit()
    
    return redirect(url_for('abm_products.index'))


    
