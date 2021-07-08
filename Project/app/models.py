from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True) # ID como primary key
    email = db.Column(db.String(100), unique=True) # Email como tipo único
    password = db.Column(db.String(100))           # Contraseña hasta 100 caracteres
    name = db.Column(db.String(100))               # Nombre del usuario
    
class SKU(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    SKUID = db.Column(db.String(10)) # ID del producto
    userID = db.Column(db.Integer)               # ID del user que puede acceder a este valor
    description = db.Column(db.String(100))      # Descripción del MELI
    price = db.Column(db.Float)                  # Precio en pesos del producto
    image = db.Column(db.String(36))             # HASH con el nombre de la imagen
    def __init__(self, **kwargs):
        super(SKU, self).__init__(**kwargs)
        
class BuyOrder(db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    IDOrder = db.Column(db.Integer) # ID de la orden de compra
    IDReceipt = db.Column(db.Integer)              # ID de la orden de recepción
    userID = db.Column(db.Integer)                 # ID del user que puede acceder a este valor
    SKU = db.Column(db.JSON)                       # JSON con todos los SKUs en esta orden
    IDProvider = db.Column(db.Integer)               # ID del proveedor  
    date = db.Column(db.DateTime)
    def __init__(self, **kwargs):
        super(BuyOrder, self).__init__(**kwargs)

class ReceiptOrder(db.Model):
    ID = db.Column(db.Integer, primary_key=True) # Id default para el sql alchemy
    IDReceipt = db.Column(db.Integer)            # ID de la orden de recepción
    userID = db.Column(db.Integer)               # ID del user que puede acceder a este valor
    date = db.Column(db.DateTime)
    def __init__(self, **kwargs):
        super(ReceiptOrder, self).__init__(**kwargs)

class Providers(db.Model):
    ID = db.Column(db.Integer, primary_key = True) 
    IDProvider = db.Column(db.Integer)             # ID del proveedor
    userID = db.Column(db.Integer)                 # ID del user que puede acceder a este valor
    name = db.Column(db.String(100))               # Nombre del proveedor
    phoneNumber = db.Column(db.Integer)            # N° telefónico del proveedor
    email = db.Column(db.String(100))              # Email del proveedor
    def __init__(self, **kwargs):
        super(Providers, self).__init__(**kwargs)
