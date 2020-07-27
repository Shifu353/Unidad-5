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
    if "DNI" in session and "Tipo" in session:
        return render_template('index.html', Tipo = escape(session['Tipo']), DNI = escape(session['DNI']) )
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


if __name__ == "__main__":
    app.run(debug=True)
