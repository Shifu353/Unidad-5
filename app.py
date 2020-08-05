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
        return render_template('principal.html', Tipo = escape(session['Tipo']))
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
                pasaword = request.form["password"]
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
            if session["Tipo"] == "Cocinero":
                pedidos = ItemsPedidos.query.all()
                return render_template('listar_pedidos_cocinero.html', pedidos=pedidos)
    else:
        listapedidos.clear()
        listaprecios.clear()
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
                p = basedatos.session.query(Pedidos).count()
                p += 2
                pedido_nuevo = Pedidos(NumPedido = "{}".format(int(p)),Fecha = datetime.date.today(), Total = total, Cobrado = 'False', Observacion=request.form['observacion'], Mesa = request.form['Mesa'],  DniMozo = escape(session["DNI"]))
                basedatos.session.add(pedido_nuevo)
                basedatos.session.commit()
                #print(pedido_nuevo.NumPedido)
                #q = basedatos.session.query(ItemsPedidos).count()
                #print(q)
                for item in range(len(listapedidos)):
                    q = basedatos.session.query(ItemsPedidos).count()
                    q += 2
                    if listapedidos[item] == "Pizza Muzarrella": 
                        producto = Productos.query.filter_by(Nombre = "Pizza Muzarrella").first()
                        nuevo_item = ItemsPedidos(NumItem = "{}".format(int(q)), NumPedido=pedido_nuevo.NumPedido,NumProducto="{}".format(int(1)), Precio=producto.PrecioUnitario, Estado="Pendiente")
                        basedatos.session.add(nuevo_item)
                    else:
                        if listapedidos[item] == "Gaseosa":
                            producto = Productos.query.filter_by(Nombre = "Gaseosa").first()
                            nuevo_item = ItemsPedidos(NumItem = "{}".format(int(q)),NumPedido=pedido_nuevo.NumPedido, NumProducto="{}".format(int(2)), Precio=producto.PrecioUnitario, Estado="Pendiente")
                            basedatos.session.add(nuevo_item)
                        else:
                            if listapedidos[item] == "Cerveza":
                                producto = Productos.query.filter_by(Nombre = "Cerveza").first()
                                nuevo_item = ItemsPedidos(NumItem = "{}".format(int(q)),NumPedido=pedido_nuevo.NumPedido, NumProducto="{}".format(int(3)), Precio=producto.PrecioUnitario, Estado="Pendiente")
                                basedatos.session.add(nuevo_item)
                            else:
                                if listapedidos[item] == "Lomo":
                                    producto = Productos.query.filter_by(Nombre = "Lomo").first()
                                    nuevo_item = ItemsPedidos(NumItem = "{}".format(int(q)),NumPedido=pedido_nuevo.NumPedido, NumProducto="{}".format(int(4)), Precio=producto.PrecioUnitario, Estado="Pendiente")
                                    basedatos.session.add(nuevo_item) 
                basedatos.session.commit()
                del listapedidos[:]
                del listaprecios[:]
                return redirect(url_for('registarPedido'))
        else:
            return redirect(url_for('login'))
@app.route("/listado_pedidos")
def Listado ():
    if "DNI" in session and "Tipo" in session:
        if escape(session['Tipo']) == "Cocinero":
            q = basedatos.session.query(Pedidos).join(ItemsPedidos).filter(ItemsPedidos.Estado == "Pendiente").all()
            for i in q:
                print(i.item_pedido)
            return render_template("listar_pedidos_cocinero.html", pedidos = q)
        
        else:
            return redirect(url_for("Logout"))    
    else:
        return redirect(url_for('login'))

@app.route('/listar <nombre> <precio>')
def Listar(nombre,precio):
    i=0
    try:
        Total=0
        productos = Productos.query.all()
        if(nombre not in listapedidos):
            listapedidos.append(nombre)
            listaprecios.append(int(precio))
       
        if(listaprecios != None):
            for i in range(len(listaprecios)):
                Total+=listaprecios[i]

        if(len(listapedidos)!=0):
            return render_template('registar_pedido_mozo.html',productos=productos,listaNom=listapedidos,total=Total)
    except(TypeError):
        print("")
#Listar Cocinero
@app.route("/ListarPedido")
def ListarCocinero ():
    if "DNI" in session and "Tipo" in session:
        if escape(session["Tipo"]) == "Cocinero":
            union = basedatos.session.query(Pedidos).join(ItemsPedidos).\
                filter(ItemsPedidos.Estado == "Pendiente").all()
            p = Pedidos.query.all()
            #print(union)
            return render_template("listar_pedidos_cocinero.html", pedidos = union)
        elif escape(session['Tipo']) == "Mozo":
            fecha_de_hoy = datetime.date.today()
            print(fecha_de_hoy)
            pedidos = Pedidos.query.filter_by(Fecha = fecha_de_hoy,Cobrado="False").all()
            return render_template('Listar_mozo.html', pedidos = pedidos)
    else:
        return redirect(url_for("/Logout"))

@app.route("/ListarPedido <int:numpedido>")
def Cocinero (numpedido):
    if "DNI" in session and "Tipo" in session:
        if escape(session["Tipo"]) == "Cocinero":
            marcar_Listo = ItemsPedidos.query.filter_by(NumItem = "{}".format(int(numpedido))).first()
            #print(marcar_Listo)
            marcar_Listo.Estado = "Listo"
            basedatos.session.commit()
            return redirect(url_for("ListarCocinero"))
        else:
            redirect(url_for("Logout"))
    else:
        return redirect(url_for("login"))
#COBRAR PEDIDO
@app.route("/CobrarPedido <int:pedido>")
def Cobrar (pedido):
    if "DNI" in session and "Tipo" in session:
        if escape(session['Tipo']) == "Mozo":
            cobrar = Pedidos.query.filter_by(NumPedido="{}".format(int(pedido))).first()
            if cobrar is not None:
                return render_template("cobrar_pedido_mozo.html",pedido = cobrar)
            else:
                return redirect(url_for("ListarCocinero"))
        else:
            return redirect(url_for("Logout"))
    else:
        redirect(url_for("Login"))
@app.route("/CobrarPedido <pedido>",methods=["POST"])
def PagarPedido (pedido):
    if "DNI" in session and "Tipo" in session:
        if escape(session["Tipo"]) == "Mozo":
            if request.method == "POST":
                cobrar = Pedidos.query.filter_by(NumPedido = "{}".format(int(pedido))).first()
                cobrar.Cobrado = "True"
                basedatos.session.commit()
                return redirect(url_for("ListarCocinero"))
        else:
            return redirect(url_for("Logout"))
    else:
        return redirect(url_for("Login"))
@app.route('/Logout')
def Logout():
    session.pop('DNI')
    session.pop('Tipo')
    listapedidos.clear()
    listaprecios.clear()
    return redirect(url_for('login'))


if __name__ == "__main__": 
    app.run(debug=True)






    ###SEGUIR CON ESTE CTM Hacelo sin un From Y aqui sin un POST
    ### Arrreglar NumPedido en el Registrar Nuevo Pedido
