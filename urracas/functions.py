# -*- coding: utf-8 -*-

from flask import request, session, g, flash, redirect, url_for
from flask.ext.mail import Message
from datetime import datetime
import requests
import json
import re
import hashlib
import math
from apikey import apikey, mapbox_token
from . import app, mail

cartodb_url = "http://jotegui.cartodb.com/api/v2/sql"

def cartodb_api(q):
    r = requests.get(cartodb_url, params={'api_key':apikey, 'q':q})
    return r

def comprobar_registro(admin=False):
    if 'usuarioId' not in session.keys():
        return False
    elif admin is True and session['rol'] != 0:
        return False
    else:
        return True


def login(admin=False):
    if admin is False:
        if 'email' not in request.form.keys() or request.form['email'] == '':
            flash("Por favor, introduce tu dirección de correo electrónico en el campo 'Email'".decode('utf-8'))
        elif 'login' not in request.form.keys():
            flash("Por favor, pulsa en la imagen del ave con la que te registraste.")
        elif admin is False:
            cur = g.db.execute('select distinct email from usuarios where activo=1;')
            usuarios = [x[0] for x in cur.fetchall()]
            if request.form['email'] not in usuarios:
                flash("Lo sentimos, pero las credenciales no son correctas. Si no te acuerdas de con qué dirección de correo electrónico te registraste o de qué ave seleccionaste, mándanos un email.".decode('utf-8'))
            else:
                cur = g.db.execute("select id, name, role, email from usuarios where activo=1 and email=? and login=?", [request.form['email'], request.form['login']]).fetchall()
                if len(cur) != 1:
                    flash("Lo sentimos, pero las credenciales no son correctas. Si no te acuerdas de con qué dirección de correo electrónico te registraste o de qué ave seleccionaste, mándanos un email.".decode('utf-8'))
                else:
                    session['usuarioId'] = cur[0][0]
                    session['nombre'] = cur[0][1]
                    session['rol'] = cur[0][2]
                    session['email'] = cur[0][3]
                    return True
    elif admin is True:
        contra = request.form['contra'].encode('utf-8')
        m = hashlib.md5()
        m.update(contra)
        c = m.hexdigest()
        d = g.db.execute("select contra from usuarios where id=?", [session['usuarioId']]).fetchone()[0]
        if c == d:
            return True
        else:
            flash("CUIDADO: Clave incorrecta")
            return False
    return False


def logout():
    print "Hello"
    session.pop('usuarioId', None)
    session.pop('nombre', None)
    session.pop('rol', None)
    flash("Has salido del sistema.")
    return


def nueva_alta():
    email = request.form['email']
    email2 = request.form['email2']
    nombre = request.form['nombre']
    
    if email == '' or email2 == '':
        flash("CUIDADO: Introduce tu correo electrónico en los dos campos.".decode('utf-8'))
        return False    
    elif email2 != email:
        flash("CUIDADO: los correos electrónicos no coinciden.".decode('utf-8'))
        return False
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash("CUIDADO: el correo electrónico no es válido.".decode('utf-8'))
        return False
    elif nombre == "":
        flash("CUIDADO: Falta que nos indiques tu nombre.")
        return False
    if 'login' not in request.form.keys():
        flash("CUIDADO: pulsa sobre la imagen de un ave para el registro.")
        return False
    
    login = request.form['login']
    ip = request.remote_addr
    
    existe = g.db.execute("SELECT count(*) FROM usuarios WHERE email=? and activo=1", [email]).fetchone()[0]
    if existe > 0:
        flash("CUIDADO: Esa dirección de correo electrónico ya está registrada. Si no recuerdas cómo entrar, escríbenos a un email.".decode('utf-8'))
        return False
    
    pre_insert_count = g.db.execute('select count(*) from usuarios where activo=1;').fetchone()[0]
    
    g.db.execute("INSERT INTO usuarios (role, name, email, login, ip, activo) VALUES (1, ?, ?, ?, ?, 1)", [nombre, email, login, ip])
    
    post_insert_count = g.db.execute('select count(*) from usuarios where activo=1;').fetchone()[0]
    if post_insert_count-pre_insert_count == 1:
        flash("Gracias, el nuevo usuario ha sido registrado en la base de datos. Para acceder al sistema, introduce tu correo electrónico, pulsa sobre la imagen del ave que seleccionaste y luego pulsa en \"Entrar\".".decode('utf-8'))
        
        # Email a admins
        destino = "MASTER"
        asunto = "Nueva alta en el sistema"
        cuerpo = "Un nuevo usuario ha sido dado de alta en el sistema:\n\nNombre: {0}\nEmail: {1}".format(nombre.encode('utf-8'), email)
        enviar_email(destino, asunto, cuerpo)
        
        # Email a usuario
        destino = email
        asunto = "Alta en en el proyecto Urracas Urbanas".decode('utf-8')
        cuerpo = """Enhorabuena, {0}, te acabas de dar de alta en la aplicación de Urracas Urbanas de Pamplona.

A partir de ahora puedes acceder al sistema y comenzar a informarnos sobre las urracas que veas por Pamplona. Para ello, sólo tienes que ir a la dirección http://www.unav.es/urracas y acceder con tu dirección de correo electrónico (ésta) y la imagen del ave que has seleccionado al darte de alta. Si en algún momento te olvidas del ave que seleccionaste, no te preocupes, envíanos un email y te la recordaremos. Igualmente, no dudes en enviarnos un email para cualquier duda o sugerencia que quieras comunicarnos.

¡Gracias por tu colaboración!

Un saludo,
El equipo del proyecto Urracas Urbanas
""".format(nombre.encode('utf-8'))
        enviar_email(destino, asunto, cuerpo)
        
        g.db.commit()
        
        return True
    else:
        flash("CUIDADO: Algo ha ido mal en el registro. Por favor, comprueba que los datos del formulario son correctos. Si sigues teniendo problemas, mándanos un correo electrónico".decode('utf-8'))
        return False


def registrar_avistamiento():
    usuarioId = session['usuarioId']

    momento = request.form['momento'] if 'momento' in request.form and request.form['momento'] != '' else 'CUIDADO: Debes indicar una fecha y hora'
    lat = request.form['lat'] if 'lat' in request.form and request.form['lat'] != '' else 'CUIDADO: Debes indicar un punto en el mapa'
    lng = request.form['lng'] if 'lng' in request.form and request.form['lng'] != '' else 'CUIDADO: Debes indicar un punto en el mapa'
    
    if momento.startswith('CUIDADO'):
        flash(momento)
        return True
    elif lat.startswith('CUIDADO') or lng.startswith('CUIDADO'):
        flash(lat)
        return True
    
    conAnillas = 1 if 'conAnillas' in request.form else 0
    cuantas = int(request.form['cuantas']) if 'cuantas' in request.form and request.form['cuantas'] != "" else 1
    print cuantas
    RT = request.form['RT'] if 'RT' in request.form else ''
    LB = request.form['LB'] if 'LB' in request.form else ''
    LT = request.form['LT'] if 'LT' in request.form else ''
    extraAnillas = 1 if 'extraanilla' in request.form else 0
    RM = request.form['RM'] if 'RM' in request.form else ''
    actividad = 'muerta' if 'muerta' in request.form else request.form['actividad']
    lectura = request.form['lectura']
    ip = request.remote_addr
    
    # LOCAL INSERT
    pre_insert_count = g.db.execute('select count(*) from avistamientos;').fetchone()[0]
    g.db.execute('INSERT INTO avistamientos (usuarioId, momento, lat, lng, conAnillas, cuantas, RT, LB, LT, extraAnillas, RM, actividad, lectura, IP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [usuarioId, momento, lat, lng, conAnillas, cuantas, RT, LB, LT, extraAnillas, RM, actividad, lectura, ip])
    post_insert_count = g.db.execute('select count(*) from avistamientos;').fetchone()[0]
    if post_insert_count-pre_insert_count == 1:
        flash("Gracias, tu avistamiento ha sido incluido en la base de datos.")
    else:
        flash("CUIDADO: Algo ha ido mal en el registro. Por favor, comprueba que los datos del formulario son correctos.")
    
    # CARTODB INSERT
    q = "INSERT INTO avistamientos (ds, ii, _is, momento, the_geom) VALUES ('{0}', '{1}', '{2}', '{3}', ST_SetSRID(ST_Point({4}, {5}), 4326))".format(RT, LB, LT, momento, lng, lat)
    res = cartodb_api(q)
    g.db.commit()
    
    return False


def comprobar_apadrinar():
    RT = request.form['RT'] if 'RT' in request.form else ''
    LB = request.form['LB'] if 'LB' in request.form else ''
    LT = request.form['LT'] if 'LT' in request.form else ''
    if RT == "" and LB == "" and LT == "":
        return False
    
    idcolor = g.db.execute("SELECT idcolor FROM datos_urracas WHERE ds=? and ii=? and _is=? limit 1", [RT, LB, LT]).fetchone()
    
    try:
        idcolor = idcolor[0]
        res = g.db.execute("SELECT nombre FROM apadrinamientos WHERE idcolor=?", [idcolor]).fetchone()

        try:
            apadrinado = res[0]
        except TypeError:
            apadrinado = ""
        if apadrinado == "":
            session.pop('idcolor', None)
            session['idcolor'] = idcolor
            return True
        else:
            flash(u"<strong>Por cierto, acabas de ver a {0}</strong>".format(apadrinado))
            return False
    except TypeError:
        return False


def apadrinar():
    usuarioId = session['usuarioId']
    ip = request.remote_addr
    nombre = request.form['apadrinado'] if 'apadrinado' in request.form and request.form['apadrinado'] != '' else 'null'
    if nombre != 'null' and request.form['apadrinar'] == 'si':
        existe = g.db.execute("SELECT count(*) from apadrinamientos where nombre=?", [nombre]).fetchone()[0]
        if existe > 0:
            flash("CUIDADO: Ese nombre ya ha sido elegido para otra urraca. Por favor, elige otro.")
            return False
        g.db.execute("INSERT INTO apadrinamientos (usuarioId, idcolor, nombre, IP) VALUES (?, ?, ?, ?);", [usuarioId, session['idcolor'], nombre, ip])
        g.db.commit()
        session.pop('idcolor', None)
        flash('Gracias. Tu petición de apadrinamiento ha sido registrada. En cuanto veamos si el nombre es adecuado, se lo asignaremos a la urraca'.decode('utf-8'))
    return True
    
    
def registrar_nido():
    usuarioId = session['usuarioId']
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    table = request.form['nidoDormidero']
    ip = request.remote_addr
    
    # Pre-check: comprobar que no haya otro nido o dormidero a menos de 50 metros en el mismo año
    print "Precomprobando"
    entidades = g.db.execute('select lat, lng from {0} where strftime(\'%Y\', creado) = strftime(\'%Y\', date(\'now\'))'.format(table)).fetchall()
    print entidades
    cerca = False
    dRef = 0.0005
    for entidad in entidades:
        eLat = float(entidad[0])
        print eLat
        eLng = float(entidad[1])
        y = eLat-lat
        print eLng
        x = eLng-lng
        d = math.sqrt(y*y+x*x)
        print d
        if d < dRef:
            cerca = True
            print "cerca"
            break
    if cerca is True:
        flash("Gracias, pero uno de los {0} registrados este año está a menos de 50 metros del que nos has indicado. Lo más probable es que se trate del mismo.".format(table).decode('utf-8'))
        return
    
    pre_insert_count = g.db.execute('select count(*) from {0};'.format(table)).fetchone()[0]
    
    g.db.execute("INSERT INTO {0} (usuarioId, lat, lng, IP) VALUES (?, ?, ?, ?)".format(table), [usuarioId, lat, lng, ip])
    
    post_insert_count = g.db.execute('select count(*) from {0};'.format(table)).fetchone()[0]
    if post_insert_count-pre_insert_count == 1:
        flash("Gracias, el registro ha sido incluido en la base de datos.")
    else:
        flash("CUIDADO: Algo ha ido mal en el registro. Por favor, comprueba que los datos del formulario son correctos.")
    g.db.commit()
    
    return


def extraer_datos(metal):
    
    if session['rol'] == 1:
        aves = {x[0]:x[1] for x in g.db.execute("select metal, buennombre from (select base.metal, base.colores, case when ap.buennombre is null then '' else ap.buennombre end as buennombre from (select distinct idcolor, metal, metal||' / '||ds||' / '||case (ii) when '' then '<nada>' else ii end||' / '||case (_is) when '' then '<nada>' else _is end as colores from datos_urracas) as base inner join (select idcolor, case (nombre) when '' then '' else nombre end as buennombre from apadrinamientos where validado=1) as ap using(idcolor)) as final order by metal;").fetchall()}
    else:
        aves = {x[0]:x[1] for x in g.db.execute("select metal, colores||' - '||buennombre from (select base.metal, base.colores, case when ap.buennombre is null then '' else ap.buennombre end as buennombre from (select distinct idcolor, metal, metal||' / '||ds||' / '||case (ii) when '' then '<nada>' else ii end||' / '||case (_is) when '' then '<nada>' else _is end as colores from datos_urracas) as base left join (select idcolor, case (nombre) when '' then '' else nombre end as buennombre from apadrinamientos where validado=1) as ap using(idcolor)) as final order by metal;").fetchall()}
    metales = sorted(aves.keys())
    datos = {}
    
    # Si se ha seleccionado un ave
    if metal is not None:

        datos['metal'] = metal
        # Datos de captura sobre el ave
        datos_urraca = g.db.execute("select * from datos_urracas where metal=?", [metal]).fetchall()

        datos_captura = datos_urraca[0]
        datos['idcolor'] = datos_captura[7]

        datos['captura_coord'] = (datos_captura[1], datos_captura[2])
        datos['captura_fecha'] = datos_captura[3]
        datos['captura_hora'] = datos_captura[11]
        datos['captura_ds'] = datos_captura[8]
        datos['captura_ii'] = datos_captura[9]
        datos['captura_is'] = datos_captura[10]

        edad = datos_captura[13]
        if edad == 1:
            edad = "Encontrado en el nido"
        elif edad == 3:
            edad = "Nacido a lo largo del año".decode('utf-8')
        elif edad == 5:
            edad = "Nacido a lo largo del año pasado a".decode('utf-8')
        elif edad == 2:
            edad = "Desconocida"
        elif edad == 4:
            edad = "Al menos dos años".decode('utf-8')
        elif edad == 6:
            edad = "Al menos tres años".decode('utf-8')
        datos['captura_edad'] = edad

        sexo = datos_captura[14]
        if sexo == 'F':
            sexo = "Hembra"
        elif sexo == 'M':
            sexo = "Macho"
        else:
            sexo = "Desconocido"
        datos['captura_sexo'] = sexo

        # Datos apadrinamiento
        nombre = g.db.execute("SELECT nombre FROM apadrinamientos WHERE idcolor=?", [datos['idcolor']]).fetchone()
        datos['nombre'] = nombre[0] if nombre is not None else ""

        # Datos avistamientos
        avistamientos = g.db.execute("SELECT * FROM avistamientos WHERE RT=? and LB=? and LT=?", [datos['captura_ds'], datos['captura_ii'], datos['captura_is']]).fetchall()
        datos['avistamientos_num'] = len(avistamientos) if avistamientos is not None else 0
    
    # Para ver informacion general
    else:
        datos['usuarios'] = g.db.execute("select count(*) from usuarios where activo=1").fetchone()[0]
        datos['avistamientos'] = g.db.execute("select count(*) from avistamientos").fetchone()[0]
        datos['avistamientos_anillas'] = g.db.execute("select count(*) from avistamientos where RT is not null and RT != 'desconocido' and RT != ''").fetchone()[0]
        datos['tus_avistamientos'] = g.db.execute("select count(*) from avistamientos where usuarioId=?", [session['usuarioId']]).fetchone()[0]
        datos['nidos'] = g.db.execute("select count(*) from nidos").fetchone()[0]
        datos['tus_nidos'] = g.db.execute("select count(*) from nidos where usuarioId=?", [session['usuarioId']]).fetchone()[0]
        datos['dormideros'] = g.db.execute("select count(*) from dormideros").fetchone()[0]
        datos['tus_dormideros'] = g.db.execute("select count(*) from dormideros where usuarioId=?", [session['usuarioId']]).fetchone()[0]
        
        datos['marcadas'] = g.db.execute("select count(*) from datos_urracas").fetchone()[0]
        datos['apadrinadas'] = g.db.execute("select count(*) from apadrinamientos where validado=1").fetchone()[0]
        
        if datos['apadrinadas'] == 0:
            datos['porc_apadrinadas'] = 0
        else:
            datos['porc_apadrinadas'] = round(datos['apadrinadas']*100.00/datos['marcadas'], 2)
        try:
            datos['posicion'] = [x[0] for x in g.db.execute("select usuarioId from avistamientos group by usuarioId order by count(*) desc").fetchall()].index(session['usuarioId'])+1
        except ValueError:
            datos['posicion'] = ""
        
    return aves, metales, datos, mapbox_token


def registrar_anillamiento():
    
    fields = []
    values = []
    
    for i in request.form:
        
        values.append(request.form[i])
        
        if i == 'lat':
            i = 'coordn'
        elif i == 'lng':
            i = 'coordw'
        elif i == 'hora':
            i = 'horacapt'
        elif i == 'IS':
            i = '_is'
        else:
            i = i.lower()
        
        fields.append(i)
    
    g.db.execute("insert into datos_urracas ({0}) values ({1})".format(', '.join(fields), ', '.join(['?']*len(values))), values)
    g.db.commit()
    flash("El anillamiento ha sido almacenado correctamente.")
    
    return


def registrar_relacion():
    if 'relparent' in request.form:
        g.db.execute("INSERT INTO relaciones_parentesco (usuarioId, metal_sujeto, tipo_relacion, metal_objeto) VALUES (?, ?, ?, ?)", [session['usuarioId'], request.form['sujeto'], request.form['relparent'], request.form['objeto']])
        flash('Relación de parentesco registrada'.decode('utf-8'))
        g.db.commit()
    return


def enviar_email(destino, asunto, cuerpo):
    remite = "javier.otegui@gmail.com"
    
    if destino == "MASTER":
        destino = g.db.execute('select email from usuarios where email="javier.otegui@gmail.com"').fetchone()[0]
    elif destino == "ADMINISTRADORES":
        destino = [x[0] for x in g.db.execute('select email from usuarios where role=0').fetchall()]
 
    if type(destino) != type([]):
        destino = [destino]
    asunto = "[URRACAS URBANAS] {0}".format(asunto).decode('utf-8')
    msg = Message(asunto, sender=remite, recipients=destino)
    msg.body = cuerpo.decode('utf-8')
    mail.send(msg)
    return

def resetear_cartodb():
    # Borrar tabla avistamientos en CartoDB
    q = "DELETE from avistamientos"
    sql_borrar=cartodb_url+"?api_key={0}&q={1}".format(apikey, q)
    #r = cartodb_api(q)
    #if r.status_code != 200:
    #    flash("Algo ha ido mal al borrar los datos de CartoDB\n",r.text)
    #    return
    #flash(r.text)
    
    # Preparar el cuerpo con todos los registros locales
    
    cur = g.db.execute('select RT, LB, LT, momento, lng, lat from avistamientos;')
    recs = cur.fetchall()
    vals = []
    for rec in recs:
        vals.append("('{0}', '{1}', '{2}', '{3}', ST_SetSRID(ST_Point({4}, {5}), 4326))".format(rec[0],rec[1],rec[2],rec[3],rec[4],rec[5]))
    q = "INSERT into avistamientos (ds, ii, _is, momento, the_geom) VALUES {0}".format(",".join(vals))
    
    sql_insertar = cartodb_url+"?api_key={0}&q={1}".format(apikey, q)
    # Lanzar la consulta INSERT
    #r = cartodb_api(q)
    #if r.status_code != 200:
    #    flash("Algo ha ido mal al insertar los datos de la BD local\n", r.text)
    #    return
    #flash(r.text)
    
    #flash("La BD de mapas ha sido restaurada")
    
    return sql_borrar, sql_insertar
