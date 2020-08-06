from flask import Flask, request, render_template, url_for, redirect, flash, session, escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import datetime


app=Flask(__name__)
app.config.from_pyfile('config.py')

from models import basedatos
from models import Usuarios,Pedidos,ItemsPedidos,Productos

@app.route('/')
def Inicio():
    url_for('bienvenida')
    return render_template('index.html')

@app.route('/bienvenida')
def bienvenida():
    return render_template('principal.html')

@app.route('/ingresar', methods = ['GET','POST'])
def ingresar():
    if request.method == 'POST':
        if  not request.form['user'] or not request.form['password']:
            return render_template('error.html', error="Por favor ingrese los datos requeridos")
        else:
            if(Usuarios.query.filter_by(DNI = request.form['user']).first()):
                usuario_actual= Usuarios.query.filter_by(DNI = request.form['user']).first()
                if usuario_actual is None:
                    return render_template('error.html', error="El Usuario no esta registrado")
                else:
                    clave=request.form['password']
                    result = hashlib.md5(bytes(clave, encoding='utf-8'))
                    if (usuario_actual.Clave == result.hexdigest()):
                        if usuario_actual.Tipo.lower()=='mozo':
                            return render_template('principal.html',mensaje='Mozo')
                        else:
                            if usuario_actual.Tipo.lower()=='cocinero':
                                return render_template('principal.html',mensaje='Cocinero')
                    else:
                        return render_template('error.html', error="La contraseña no es valida")
            else:
                return render_template('error.html', error="El Usuario no esta registrado")
    else:
        return render_template('index.html')

@app.route('/menu',methods=['GET','POST'])
def menu():
    listaNom=[]
    i=0
    for i in range(len(Productos.query.all())+1):
        elemento=Productos.query.filter_by(NumProducto = i).first()
        listaNom.append(elemento)
    return render_template('registro_pedido_mozo.html',lista=listaNom)
        
@app.route('/pedido',methods=['GET','POST'])
def pedido():
    pass

if __name__=='__main__':
    app.run(debug=True)
