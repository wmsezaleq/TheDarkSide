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

    def create_sku(self, userID, description):
        amount = len(SKU.query.all())
        ID = len(SKU.query.filter_by(userID=userID).all()) + 1
        SKUID = self._convertIDtoSKU(self, ID)
        data = SKU(ID=amount, SKUID=SKUID, userID=userID, description=description, price=0, image="")
        db.session.add(data)
        db.session.commit()
        return SKUID

    def _decode(self, SKUID):
        flotante = SKUID[5:]
        flotante = int(flotante)
        

    def create_product(self, userID, SKUID, description):
        amount = self._decode(self, SKUID)
        data = SKU(ID=amount, SKUID=SKUID, userID=userID, description=description, price=0, image="")
        db.session.add(data)
        db.session.commit()

    def _convertIDtoSKU(self, ID):
        decimal, flotante = str(ID / 10_000).split(".")
        for i in range(len(flotante)-5):
            flotante = "0" + flotante[:len(flotante)-1]
        conversion_table = [] # tabla de conversiones por index con carácter
        for i in range(26):
            conversion_table.append(chr(i+97))
        alphabet = "" 
        decimal = int(decimal)
        if decimal == 0:
            alphabet = "AAAAA"
        else:
            while decimal > 0:
                remainder = decimal % 26
                alphabet = conversion_table[remainder] + alphabet
                decimal = decimal // 26
            for i in range(len(alphabet) - 5):
                alphabet = "A" + alphabet[0:]
        return alphabet.upper() + flotante

        
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

    def insert_for_id(self, userID, nameProvider):
        amount = len(Providers.query.all())
        IDProvider = len(Providers.query.filter_by(userID=userID).all()) + 1
        data = Providers(ID=amount, IDProvider=IDProvider, userID=userID, name=nameProvider, phoneNumber=0, email="")
        db.session.add(data)
        db.session.commit()
        return IDProvider