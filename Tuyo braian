from flask import Flask,escape,render_template,session, url_for, request, redirect, flash
from sqlalchemy.orm import sessionmaker
import datetime
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import hashlib
from sqlalchemy.orm.session import make_transient
app = Flask(__name__)
app.config.from_pyfile("config.py")

from models import Usuarios,Pedidos, ItemsPedidos, Productos, basedatos
        
listapedidos = []
listapedidos = []
listaprecios = []
#cant = 0

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
def Nuevopedido():
    if request.method == "POST":
        if "DNI" in session and "Tipo" in session:
            if session["Tipo"] == 'Mozo':
                #Observacion = request.form['items']
                #Observacion = Observacion.split(",")
                total = 0
                for i in range(len(listaprecios)):
                    total += listaprecios[i]
                
                pedido_nuevo = Pedidos(Fecha = datetime.date.today(), Total = total, Cobrado = False, Observacion=request.form['observacion'], Mesa = request.form['Mesa'],  DniMozo = escape(session["DNI"]))
                basedatos.session.add(pedido_nuevo)
                basedatos.session.commit()
                print(Pedidos.NumPedido)
                for item in range(len(listapedidos)):
                    if listapedidos[item] == "Pizza Muzarrella": 
                        producto = Productos.query.filter_by(Nombre = "Pizza Muzarrella").first()
                        nuevo_item = ItemsPedidos(NumPedido=1, NumProducto=1, Precio=producto.PrecioUnitario, Estado="Pendiente")
                        basedatos.session.add(nuevo_item)
                    else:
                        if listapedidos[item] == "Gaseosa":
                            producto = Productos.query.filter_by(Nombre = "Gaseosa").first()
                            nuevo_item = ItemsPedidos(NumPedido=1, NumProducto=2, Precio=producto.PrecioUnitario, Estado="Pendiente")
                            basedatos.session.add(nuevo_item)
                        else:
                            if listapedidos[item] == "Cerveza":
                                producto = Productos.query.filter_by(Nombre = "Cerveza").first()
                                nuevo_item = ItemsPedidos(NumPedido=1, NumProducto=3, Precio=producto.PrecioUnitario, Estado="Pendiente")
                                basedatos.session.add(nuevo_item)
                            else:
                                if listapedidos[item] == "Lomo":
                                    producto = Productos.query.filter_by(Nombre = "Lomo").first()
                                    nuevo_item = ItemsPedidos(NumPedido=1, NumProducto=4, Precio=producto.PrecioUnitario, Estado="Pendiente")
                                    basedatos.session.add(nuevo_item) 
                basedatos.session.commit()
                return "FASJBFJDABSFJLDBSJLFDSJLFN"
                #return redirect(url_for('registarPedido'))
        else:
            return redirect(url_for('login'))

@app.route("/listado_pedidos")
def Listado ():
    if "DNI" in session and "Tipo" in session:
        if escape(session['Tipo']) == "Cocinero":
            item = ItemsPedidos.query.filter_by(Estado = "Pendiente")
            print(item)
            return "JSDLAFNJLASBFKJBSJBF"

@app.route('/listar <nombre> <precio>')
def Listar(nombre,precio):
    i=0
    cant=0
    try:
        Total=0
        productos = Productos.query.all()
        #print(nombre)
        #print(precio)
        if(nombre not in listapedidos):
            listapedidos.append(nombre)
            listaprecios.append(int(precio))
        else:
            listaprecios.append(int(precio))
        if(listaprecios != None):
            for i in range(len(listaprecios)):
                Total+=listaprecios[i]

        if(cant <= 1):
            if(len(listapedidos)!=0):
                return render_template('registar_pedido_mozo.html',productos=productos,listaNom=listapedidos,total=Total)
        else:
            return render_template('registar_pedido_mozo.html',productos=productos,listaNom=listapedidos,total=Total,cantidad=cant)
    except(TypeError):
        print("")


@app.route('/Logout')
def Logout():
    session.pop('DNI')
    session.pop('Tipo')
    listapedidos.clear()
    listaprecios.clear()
    return render_template("login.html")


if __name__ == "__main__": 
    app.run(debug=True)
