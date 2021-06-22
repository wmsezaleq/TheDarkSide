from enum import unique
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True) # ID como primary key
    email = db.Column(db.String(100), unique=True) # Email como tipo único
    password = db.Column(db.String(100)) # Contraseña hasta 100 caracteres
    name = db.Column(db.String(1000)) # Nombre del usuario
    