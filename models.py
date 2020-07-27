from __main__ import app
from flask_sqlalchemy import SQLAlchemy

basedatos=SQLAlchemy(app)

class Productos(basedatos.Model):
    NumProducto= basedatos.Column(basedatos.Integer,primary_key=True)
    Nombre= basedatos.Column(basedatos.String(120),nullable=False)
    PrecioUnitario= basedatos.Column(basedatos.Float,nullable=False)
    item_producto=basedatos.relationship('ItemsPedidos',backref='productos',lazy='dynamic')
class ItemsPedidos(basedatos.Model):
    NumItem= basedatos.Column(basedatos.Integer,primary_key=True)
    NumPedido=basedatos.Column(basedatos.Integer,basedatos.ForeignKey('pedidos.NumPedido'))
    NumProducto=basedatos.Column(basedatos.Integer,basedatos.ForeignKey('productos.NumProducto'))
    Precio=basedatos.Column(basedatos.Float,nullable=False)
    Estado=basedatos.Column(basedatos.String(50),nullable=False)

class Pedidos(basedatos.Model):
    NumPedido= basedatos.Column(basedatos.Integer,primary_key=True)
    Fecha= basedatos.Column(basedatos.DateTime)
    Total= basedatos.Column(basedatos.Float,nullable=False)
    Cobrado= basedatos.Column(basedatos.String(2),nullable=False)
    Observacion=basedatos.Column(basedatos.Text)
    DniMozo=basedatos.Column(basedatos.Integer,basedatos.ForeignKey('usuarios.DNI'))
    Mesa=basedatos.Column(basedatos.Integer,nullable=False,unique=True)
    item_pedido=basedatos.relationship('ItemsPedidos',backref='pedidos',lazy='dynamic')

class Usuarios(basedatos.Model):
    DNI=basedatos.Column(basedatos.String(16),primary_key=True)
    Clave=basedatos.Column(basedatos.String(16),nullable=False,unique=True)
    Tipo=basedatos.Column(basedatos.String(16),nullable=False,unique=True)    
    pedido_cargado = basedatos.relationship('Pedidos',backref='usuarios',lazy='dynamic')
