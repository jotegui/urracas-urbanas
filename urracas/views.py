# -*- coding: utf-8 -*-

import os
import hashlib
from flask import render_template, redirect, url_for, request, flash, session, g
from . import app, db
from . import functions as f

@app.route("/")
def main():
    session.pop('_flashes', None)
    return render_template("index.html")


@app.route("/instrucciones")
def instrucciones():
    return render_template("usuario/instrucciones.html")


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    admin = False
    if request.method == 'POST':
        if 'contra' not in request.form:
            login = f.login()
            if login is True:
                if session['rol'] == 1:
                    return redirect(url_for('inicio'))
                else:
                    admin=True
        else:
            admin=True
            login = f.login(admin=True)
            if login is True:
                return redirect(url_for('inicio'))
    return render_template("registro.html", admin=admin)


@app.route("/alta", methods=['GET', 'POST'])
def alta():
    if request.method == 'POST':
        registrado = f.nueva_alta()
        if registrado is True:
            return redirect(url_for('registro'))
    return render_template("alta.html")


@app.route("/inicio")
def inicio():
    registro = f.comprobar_registro()
    if registro is False:
        return redirect(url_for('registro'))
    return render_template("inicio.html")


@app.route("/salir")
def salir():
    f.logout()
    return redirect(url_for('registro'))


@app.route("/formulario", methods=['GET', 'POST'])
def formulario():
    registro = f.comprobar_registro()
    if registro is False:
        return redirect(url_for('registro'))
    
    codigos = [str(x[0]) for x in g.db.execute('SELECT DISTINCT ds||"-"||ii||"-"||_is as codigo from datos_urracas;').fetchall()]
    
    if request.method == 'POST' and 'apadrinar' not in request.form.keys():
        actividad, fallo = f.registrar_avistamiento()
        if fallo is True:
            return redirect(url_for('formulario'))
        if actividad != 'muerta':
            apadrinar = f.comprobar_apadrinar()
            if apadrinar is True:
                return redirect(url_for('apadrinar'))
    elif request.method == 'POST' and 'apadrinar' in request.form.keys():
        exito = f.apadrinar()
        if exito is False:
            return redirect(url_for('apadrinar'))
    
    return render_template("usuario/formulario.html", codigos=codigos)


@app.route("/apadrinar")
def apadrinar():
    registro = f.comprobar_registro()
    if registro is False:
        return redirect(url_for('registro'))
    
    if 'idcolor' not in session.keys():
        return redirect(url_for('inicio'))
    
    sexo_clave = g.db.execute("select sexo from datos_urracas where idcolor=?", [session['idcolor']]).fetchone()[0]
    if sexo_clave == 'M':
        sexo = 'macho'
    elif sexo_clave == 'H':
        sexo = 'hembra'
    else:
        sexo = 'que no sabemos si es macho o hembra'
    
    return render_template("usuario/apadrinamiento.html", sexo=sexo)


@app.route("/nidosdormideros", methods=['GET','POST'])
def nidosdormideros():
    registro = f.comprobar_registro()
    if registro is False:
        return redirect(url_for('registro'))
    
    otro = ""
    if request.method == 'POST':
        f.registrar_nido()
        otro = " otro"
    
    return render_template("usuario/nidosdormideros.html", otro=otro)


@app.route("/info")
def info(metal=None):
    registro = f.comprobar_registro()
    if registro is False:
        return redirect(url_for('registro'))

    metal=request.args.get("metal") if "metal" in request.args else None
    print metal
    aves, metales, datos, mapbox_token = f.extraer_datos(metal)
    
    return render_template('usuario/info.html', metales=metales, aves=aves, datos=datos, mapbox_token=mapbox_token)


@app.route("/mis_observaciones")
def mis_observaciones():
    registro = f.comprobar_registro()
    if registro is False:
        return redirect(url_for('registro'))
    
    obs = g.db.execute("select momento, lat, lng, conAnillas, RT, LB, LT, actividad, lectura from avistamientos where usuarioId=?", [session['usuarioId']]).fetchall()
    
    return render_template('usuario/mis_observaciones.html', obs=obs)



if __name__ == "__main__":
    app.run()
