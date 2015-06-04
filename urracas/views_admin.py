# -*- coding: utf-8 -*-

import os
import hashlib
from flask import render_template, redirect, url_for, request, flash, session, g
from . import app, db
from . import functions as f


### ZONA ADMINISTRADOR


@app.route("/aprobar", methods=['GET', 'POST'])
def aprobar():
    registro = f.comprobar_registro(admin=True)
    if registro is False:
        return redirect(url_for('registro'))
    
    if request.method == 'POST':
        if 'id' in request.form and 'accion' in request.form:
            nombre = g.db.execute("select nombre from apadrinamientos where id=?", [request.form['id']]).fetchone()[0]
            if request.form['accion'] == 'aprobar':
                g.db.execute("update apadrinamientos set validado=1 where id=?", [request.form['id']])
                flash("Nombre validado")
            elif request.form['accion'] == 'denegar':
                g.db.execute("delete from apadrinamientos where id=?", [request.form['id']])
                flash("Nombre eliminado")
            else:
                flash("CUIDADO: Algo ha ido mal. Comprueba los logs o pregunta al administrador")
            g.db.commit()
    
    nombres = g.db.execute("select a.id, b.email, a.nombre, a.IP, a.creado from apadrinamientos as a left join usuarios as b on a.usuarioId = b.id where a.validado=0 order by a.creado").fetchall()
    
    return render_template('admin/aprobar.html', nombres=nombres)


@app.route("/gestionusuarios", methods=['GET','POST'])
def gestionusuarios():
    registro = f.comprobar_registro(admin=True)
    if registro is False:
        return redirect(url_for('registro'))
    
    if request.method == 'POST':
                
        if 'id' in request.form and 'accion' in request.form:
                        
            if request.form['accion'] == 'eliminar':
                g.db.execute("update usuarios set activo=0 where id=?", [request.form['id']])
                flash("Usuario desactivado. Sus datos y observaciones NO han sido eliminados")
                g.db.commit()
            
            elif request.form['accion'] == 'promocionar':
                g.db.execute("update usuarios set role=0 where id=?", [request.form['id']])
                contra = request.form['contra'].encode('utf-8')
                m = hashlib.md5()
                m.update(contra)
                c = m.hexdigest()
                g.db.execute("update usuarios set contra=? where id=?", [c, request.form['id']])
                flash("Usuario promocionado a administrador")
                g.db.commit()
            
            elif request.form['accion'] == 'degradar':
                g.db.execute("update usuarios set role=1 where id=?", [request.form['id']])
                g.db.execute("update usuarios set contra=null where id=?", [request.form['id']])
                flash("Administrador degradado a usuario")
                g.db.commit()
                
        elif 'destino' in request.form and 'asunto' in request.form and 'cuerpo' in request.form:
            destino = [request.form['destino']]
            asunto = "Mensaje de {0}: ".format(session['email'])
            asunto += request.form['asunto'].encode('utf-8')
            cuerpo = request.form['cuerpo'].encode('utf-8')
            f.enviar_email(destino=destino, asunto=asunto, cuerpo=cuerpo)
            flash("Mensaje enviado")    
            
    usuarios = g.db.execute("select id, case role when 0 then 'Administrador' when 1 then 'Usuario' end as role, name, email, case login when 1 then 'Pato' when 2 then 'Urraca' when 3 then 'Mirlo' when 4 then 'Gorrion' when 5 then 'Paloma' when 6 then 'Petirrojo' when 7 then 'Carbonero' when 8 then 'Cernicalo' when 9 then 'Vencejo' end as login, IP, creado from usuarios where activo=1;").fetchall()
    
    return render_template('admin/gestionusuarios.html', usuarios=usuarios)


@app.route("/formulariocampo", methods=['GET', 'POST'])
def formulariocampo():
    registro = f.comprobar_registro(admin=True)
    if registro is False:
        return redirect(url_for('registro'))
    
    if request.method == 'POST':
        f.registrar_anillamiento()
    
    return render_template('admin/formulariocampo.html')


@app.route("/relaciones", methods=['GET', 'POST'])
def relaciones():
    registro = f.comprobar_registro(admin=True)
    if registro is False:
        return redirect(url_for('registro'))
    
    if request.method == 'POST':
        f.registrar_relacion()
        pass
    
    metales = g.db.execute("select distinct metal from datos_urracas order by metal;").fetchall()
    relaciones = g.db.execute("select * from relaciones_parentesco_tipos;").fetchall()
    
    return render_template('admin/relaciones.html', metales=metales, relaciones=relaciones)


@app.route("/gestiondatos", methods=['GET', 'POST'])
def gestiondatos():
    registro = f.comprobar_registro(admin=True)
    if registro is False:
        return redirect(url_for('registro'))
    
    if request.method == 'POST':
        if 'id' in request.form and 'accion' in request.form:
            if request.form['accion'] == 'eliminar':
                g.db.execute("delete from avistamientos where id=?", [request.form['id']])
                flash("Avistamiento eliminado.")
                g.db.commit()
    
    encAvistamientos = ['id','usuarioId','usuario','usuarioActivo','momento','lat','lng','conAnillas','derechaSuperior','izquierdaInferior','izquierdaSuperior','anillaExtra','derechaMedio','actividad','modoLectura','cantidad','apadrinadoPor','apadrinadoComo','validado']
    avistamientos = g.db.execute('select a.id as id, a.usuarioId as usuarioId, a.email as usuario, a.activo as usuarioActivo, a.momento as momento, a.lat as lat, a.lng as lng, a.conAnillas as conAnillas, a.RT as derechaSuperior, a.LB as izquierdaInferior, a.LT as izquierdaSuperior, a.extraAnillas as anillaExtra, a.RM as derechaMedio, a.actividad as actividad, a.lectura as modoLectura, a.cuantas as cantidad, p.usuarioID as apadrinadoPor, p.nombre as apadrinadoComo, p.validado as apadrinamientoValidado from (select * from (select * from avistamientos) as a left join (select * from usuarios) as u on a.usuarioId = u.id) as a left join (select * from apadrinamientos) as p using (usuarioId);').fetchall()
    
    return render_template('admin/gestiondatos.html', encAvistamientos=encAvistamientos, avistamientos=avistamientos)

@app.route("/gestionanillamientos", methods=['GET', 'POST'])
@app.route("/gestionanillamientos/<id>", methods=['GET', 'POST'])
def gestionanillamientos(id=0):
    registro = f.comprobar_registro(admin=True)
    if registro is False:
        return redirect(url_for('registro'))
    
    if request.method == 'POST':
        if 'id' in request.form and 'accion' in request.form:
            if request.form['accion'] == 'eliminar':
                g.db.execute("delete from datos_urracas where id=?", [request.form['id']])
                flash("Registro eliminado")
                g.db.commit()
            elif request.form['accion'] == 'modificar':
                q = "update datos_urracas set "
                for i in [x for x in request.form.keys() if x.endswith('val')]:
                    k = i[:-3]
                    v = request.form[i]
                    if k in ['fecha', 'lugar', 'horaini', 'metal', 'ds', 'ii', '_is', 'dm', 'horacapt', 'sexo', 'fotocaraid', 'fototarsoid', 'plumasid', 'sangreid', 'dietaid', 'mudaactid', 'horafin', 'comentarios', 'usuario']:
                        v = "'"+v+"'"
                    q += "{0}={1}, ".format(k, v)
                q = q[:-2]
                q += " where id={0}".format(request.form['id'])
                g.db.execute(q)
                flash("Datos modificados. Por favor, comprueba que los nuevos datos son correctos.")
    
    anillamientos = g.db.execute('select * from datos_urracas;').fetchall()
    if id!=0:
        campos = g.db.execute('select * from datos_urracas where id=?', [id]).fetchone()
    else:
        campos = ()
    
    return render_template('admin/gestionanillamientos.html', id=id, anillamientos=anillamientos, campos=campos)

@app.route("/descarga", methods=["POST"])
def descarga():
    return 

@app.route("/resetcdb", methods=['GET'])
def resetcdb():
    registro = f.comprobar_registro(admin=True)
    if registro is False:
        return redirect(url_for('registro'))

    if request.method == "GET":
        sql_borrar, sql_insertar = f.resetear_cartodb()
        return render_template('admin/resetcdb.html', sql_borrar=sql_borrar, sql_insertar=sql_insertar)
    #else:
    #    f.resetear_cartodb()
    #    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run()
