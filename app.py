from flask import Flask,escape,render_template,session, url_for, request, redirect
from datetime import datetime
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config.from_pyfile("config.py")

from models import Usuarios

@app.route("/")
def index ():
    if "dni" in session and "tipo" in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route("/login")
def login ():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def LOGIN ():
    if request.method == "POST":
        if request.form["dni"] and request.form["password"]:
            usuario = Usuarios.query.filter_by(dni=request.form['dni'])
            if type(usuario) is not None:
                clave = request.form["dni"]
                result = hashlib.md5(bytes(clave, encoding='utf-8'))
                if usuario.clave == result.hexdigest():
                    session['dni'] = usuario.dni
                    session['tipo'] = usuario.tipo
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))
        

if __name__ == "__main__":
    app.run(debug=True)
"""from flask import Flask, request, render_template, url_for, redirect, session, escape, flash
from flask_sqlalchemy import SQLAlchemy
#from markupsafe import escape
from datetime import datetime
from sqlalchemy import distinct
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = "b\xdfA\xf1n\xf3Q|\xf3\xbc5oeS\xad\x19'"
app.permanent_session_lifetime 
from models import db
from models import Usuarios,Pedidos,Productos,ItemsPedidos

@app.before_request
def Permanente ():
    session.permanent = True

@app.route("/")
def index():
    if 'dni' in session and "tipo" in session:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/bienvenida')
def bienvenida():
    if "dni" in session:
        return redirect(url_for("index"))
    return render_template('principal.html')

@app.route('/ingresar', methods = ['GET','POST'])
def ingresar():
    if request.method == 'POST':
        if  not request.form['user'] or not request.form['password']:
            return render_template('error.html', error="Por favor ingrese los datos requeridos")
        else:
            if(Usuarios.query.filter_by(dni = request.form['user']).first()):
                usuario_actual= Usuarios.query.filter_by(dni = request.form['user']).first()
                if usuario_actual is None:
                    return render_template('error.html', error="El Usuario no esta registrado")
                else:
                    clave = request.form['password']
                    result = hashlib.md5(bytes(clave, encoding='utf-8'))
                    if (usuario_actual.clave == result.hexdigest()):
                        if usuario_actual.tipo.lower()=='mozo':
                            session["dni"] = usuario_actual.dni
                            session["tipo"] = usuario_actual.tipo
                            return render_template('principal.html',mensaje='Mozo')
                        else:
                            if usuario_actual.tipo.lower()=='cocinero':
                                return render_template('principal.html',mensaje='Cocinero')
                    else:
                        return render_template('error.html', error="La contraseña no es valida")
            else:
                return render_template('error.html', error="El Usuario no esta registrado")
    elif request.method == "GET":
        #print(request.args.getlist(key="HOLA"))
        return redirect("registrarPedido")
    else:
        return render_template('index.html')

@app.route("/logout")
def logout ():
    session.pop("dni", None)
    session.pop("tipo", None)
    return redirect(url_for("index"))

@app.route('/registrarPedido')
def registrarPedido():
    if "dni" in session and "tipo" in session:
        #productos = []
        if escape(session['tipo']) == "Mozo":
            productos = Productos.query.all()
            #productos.append(Productos.query.all())
            #titulo = "Registrar Pedido" 
            return render_template('registar_pedido_mozo.html',productos=productos)
        elif escape(session['tipo']) == "Cocinero":
            pass
        else :
            return redirect("logout")
    else:
        flash("Tip: Deberías Iniciar Sesión antes de realizar pedidos ;)")
        return redirect(url_for("bienvenida"))

@app.route("/registrarpedido", methods = ["POST","GET"])
def registrarpedido ():
    if request.method == "POST":
        if "dni" in session and "tipo" in session:
            items = request.form["items"]
            print(items)
            items = items.split(",")
            nuevo_pedido = Pedidos(fecha=datetime.now().date(), total= request.form['total'], cobrado= False, observacion=request.form['observacion'], Mesa=request.form['Mesa'], dnimozo=escape(session['dni']))
            db.session.add(nuevo_pedido)
           # db.session.commit()
            for item in items:
                #print(int(item))
                producto = Productos.query.filter_by(numProducto=item).first()
                if producto is None:
                    flash('Error al cargar los items.')
                    return redirect(url_for('registrarPedido'))
                else:
                    print(producto) 
                    nuevo_item = ItemsPedidos(numPedido= nuevo_pedido.numPedido, numProducto= item, precio= producto.PrecioUnitario, estado= 'Pendiente')
                    db.session.add(nuevo_item)
            db.session.commit()
            flash('Registro exitoso.')
            return redirect(url_for('registrarPedido'))
        else:
            flash('Algo no ha salido bien. Reintenta el pedido.')
            return redirect(url_for('registrarPedido'))


        
if __name__ == '__main__':
    # cifrado de la clave utilizando md5
    clave = '41830596'
    result = hashlib.md5(bytes(clave))
    # muestra la clave cifrada en hexadecimal, esta es la que se debe guardar en base de datos
    print(result.hexdigest())
    
    app.run(debug=True)"""