from flask import Flask,escape,render_template,session, url_for, request, redirect
import datetime
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config.from_pyfile("config.py")

from models import Usuarios,Pedidos, ItemsPedidos, Productos, basedatos

@app.route("/")
def index ():
    if "DNI" in session and "Tipo" in session:
        return render_template('principal.html', Tipo = escape(session['Tipo']))#, DNI = escape(session['DNI']) )
    return redirect(url_for('login'))

@app.route("/login")
def login ():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def LOGIN ():
    if request.method == "POST":
        if request.form["dni"] and request.form["password"]:
            usuario = Usuarios.query.filter_by(DNI=request.form['dni']).first()
            if type(usuario) is not None:
                pasaword = request.form["dni"]
                result = hashlib.md5(bytes(pasaword, encoding='utf-8'))
                if usuario.Clave == result.hexdigest():
                    session['DNI'] = usuario.DNI
                    session['Tipo'] = usuario.Tipo
                    print("ENTRE")
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))

@app.route("/registrarPedido")
def registarPedido ():
    if "DNI" in session:
        if session["Tipo"] == "Mozo":
            productos = Productos.query.all()
            return render_template('registar_pedido_mozo.html', productos=productos)
    else:
        return redirect(url_for('login'))

@app.route("/nuevopedido", methods=["POST"])
def nuevopedido ():
    if request.method == "POST":
        if "DNI" in session and "Tipo" in session:
            if session["Tipo"] == 'Mozo':
                items = request.form['items']
                items = items.split(",")
                pedido_nuevo = Pedidos(Fecha = datetime.date.today(), Total = request.form['total'], Cobrado = False, Observacion=request.form['observacion'], Mesa = request.form['Mesa'],  DniMozo = escape(session["DNI"]))
                basedatos.session.add(pedido_nuevo)
                basedatos.session.commit()
                for item in items:
                    producto = Productos.query.filter_by(NumProducto = int(item))
                    if producto is None:
                        return redirect(url_for('registarPedido'))
                    else:
                        nuevo_item = ItemsPedidos(NumPedido=pedido_nuevo.NumPedido, NumProducto=item, Precio=producto.PrecioUnitario, Estado="Pendiente")
                        basedatos.session.add(nuevo_item)
                basedatos.session.commit()
                redirect(url_for('registarPedido'))
        else:
            return redirect(url_for('login'))

@app.route("/listado_pedidos")
def Listado ():
    if "DNI" in session and "Tipo" in session:
        if escape(session['Tipo']) == "Cocinero":
            item = ItemsPedidos.query.filter_by(Estado = "Pendiente")
            print(item)
            return "JSDLAFNJLASBFKJBSJBF"




if __name__ == "__main__":
    app.run(debug=True)
