from flask_login import UserMixin
import sqlalchemy.types 
from . import db
import json


class User(UserMixin, db.Model):
    id = db.Column(sqlalchemy.types.Integer, primary_key = True) # ID como primary key
    email = db.Column(sqlalchemy.types.String(100), unique=True) # Email como tipo único
    password = db.Column(sqlalchemy.types.String(100))           # Contraseña hasta 100 caracteres
    name = db.Column(sqlalchemy.types.String(100))               # Nombre del usuario
    
class SKU(db.Model):
    ID = db.Column(sqlalchemy.types.Integer, primary_key=True)
    INTSKU = db.Column(sqlalchemy.types.Integer)
    SKUID = db.Column(sqlalchemy.types.String(10))             # ID del producto
    userID = db.Column(sqlalchemy.types.Integer)               # ID del user que puede acceder a este valor
    description = db.Column(sqlalchemy.types.String(100))      # Descripción del MELI
    price = db.Column(sqlalchemy.types.Float)                  # Precio en pesos del producto
    def __init__(self, **kwargs):
        super(SKU, self).__init__(**kwargs)

    def getDict(self, queryData):
        data = {}
        for sku in queryData:
            data[sku.SKUID] = {
                "Descripcion" : sku.description,
                "Precio" : sku.price,
                "Foto" : {},
                }
        return data
        
    def getMissingID(self, userID):
        IDs = []
        for row in SKU.query.filter_by(userID=userID).all():
            IDs.append(row.INTSKU)
        try:
            start = IDs[0]
            end = IDs[1]
            return sorted(set(range(start, end + 1)).difference(IDs))
        except:
            pass                                  
        return 1

    def getSKU(self, ID):
        return hex(ID).split("x")[1].zfill(10)

    def getID(self, SKUID):
        return int(SKUID, 16)


from datetime import datetime
class BuyOrder(db.Model):
    ID = db.Column(sqlalchemy.types.Integer, primary_key = True)
    IDOrder = db.Column(sqlalchemy.types.Integer) # ID de la orden de compra
    IDReceipt = db.Column(sqlalchemy.types.Integer)              # ID de la orden de recepción
    userID = db.Column(sqlalchemy.types.Integer)                 # ID del user que puede acceder a este valor
    SKU = db.Column(sqlalchemy.types.JSON)                       # JSON con todos los SKUs en esta orden
    IDProvider = db.Column(sqlalchemy.types.Integer)               # ID del proveedor  
    date = db.Column(sqlalchemy.types.DateTime)
    def __init__(self, **kwargs):
        super(BuyOrder, self).__init__(**kwargs)

    def getQuantity_Price(self, buyOrderSKU):
        cantidad = 0
        precio = 0
        for SKU in buyOrderSKU:
            data = buyOrderSKU[SKU]
            cantidad += int(data["quantity"])
            precio += (float(data["price"]) * int(data["quantity"]))
        return [cantidad, precio]
    
    def getDict(self, data, fromDate : datetime.date, toDate : datetime.date):
        orders = {}
        for buyorder in data:
            if datetime.date(buyorder.date) >= fromDate and datetime.date(buyorder.date) <= toDate:
                nombreProveedor =  Providers.query.filter_by(
                                                userID=buyorder.userID,
                                                IDProvider=buyorder.IDProvider).first().name
                cantidad, precio = BuyOrder.getQuantity_Price(BuyOrder, buyorder.SKU)
                
                orders[buyorder.IDOrder] = {
                    "IDReceipt" : buyorder.IDReceipt,
                    "SKU" : buyorder.SKU,
                    "Provider" : nombreProveedor,
                    "Date" : buyorder.date.strftime("%d/%m/%Y"),
                    "Price" : float(precio),
                    "Quantity" : cantidad
                }
        return orders

class ReceiptOrder(db.Model):
    ID = db.Column(sqlalchemy.types.Integer, primary_key=True) # Id default para el sql alchemy
    IDReceipt = db.Column(sqlalchemy.types.Integer)            # ID de la orden de recepción
    userID = db.Column(sqlalchemy.types.Integer)               # ID del user que puede acceder a este valor
    date = db.Column(sqlalchemy.types.DateTime)
    def __init__(self, **kwargs):
        super(ReceiptOrder, self).__init__(**kwargs)

class Providers(db.Model):
    ID = db.Column(sqlalchemy.types.Integer, primary_key = True) 
    IDProvider = db.Column(sqlalchemy.types.Integer)             # ID del proveedor
    userID = db.Column(sqlalchemy.types.Integer)                 # ID del user que puede acceder a este valor
    name = db.Column(sqlalchemy.types.String(100))               # Nombre del proveedor
    phoneNumber = db.Column(sqlalchemy.types.Integer)            # N° telefónico del proveedor
    email = db.Column(sqlalchemy.types.String(100))              # Email del proveedor
    def __init__(self, **kwargs):
        super(Providers, self).__init__(**kwargs)
    def getNameList(self, userID):
        data = []
        queryData = Providers.query.filter_by(userID=userID).all()
        for provider in queryData:
            data.append(provider.name)
            
        return [json.dumps(data), queryData]

class IMG(db.Model):
    ID = db.Column(sqlalchemy.types.Integer, primary_key=True)
    userID = db.Column(sqlalchemy.types.Integer)
    img = db.Column(sqlalchemy.types.Text)
    mimetype = db.Column(sqlalchemy.types.Text)
    name = db.Column(sqlalchemy.types.Text)
    SKU = db.Column(sqlalchemy.types.String(10))
    
class Deposit(db.Model):
    ID = db.Column(sqlalchemy.types.Integer, primary_key=True)
    userID = db.Column(sqlalchemy.types.Integer)
    h = db.Column(sqlalchemy.types.Integer)
    w = db.Column(sqlalchemy.types.Integer)
    lvl = db.Column(sqlalchemy.types.Integer)
    name = db.Column(sqlalchemy.types.String(6))

class Position(db.Model):
    ID = db.Column(sqlalchemy.types.Integer, primary_key=True)
    userID = db.Column(sqlalchemy.types.Integer)
    depositID = db.Column(sqlalchemy.types.Integer)
    w = db.Column(sqlalchemy.types.Integer)
    h = db.Column(sqlalchemy.types.Integer)
    type = db.Column(sqlalchemy.types.BOOLEAN)
    floor = db.Column(sqlalchemy.types.Integer)
    products = db.Column(sqlalchemy.types.JSON)
    

