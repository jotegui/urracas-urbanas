-- Tabla de usuarios
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id integer primary key autoincrement,
    role integer not null, -- 0=admin, 1=user
    name text not null,
    email text not null,
    login integer not null, -- Animal code
    contra text, -- Password solo para administradores
    IP text,
    activo boolean, -- Si el usuario esta activo o no
    creado DATETIME DEFAULT (datetime('now', 'localtime')),
    eliminado DATETIME -- momento de desactivacion
);

INSERT INTO usuarios (role, name, email, login, contra, activo) VALUES (0, 'Javier', 'javier.otegui@gmail.com', 7, 'd70e57dc6b931259281cd526ed37cd50', 1);
INSERT INTO usuarios (role, name, email, login, contra, activo) VALUES (0, 'Antonio', 'papirroyo@yahoo.es', 6, '98c1d8bb3c9f89b3ec2c1dda04998559', 1);

-- Tabla de avistamientos
DROP TABLE IF EXISTS avistamientos;
CREATE TABLE avistamientos (
    id integer primary key autoincrement,
    usuarioId integer not null,
    momento datetime not null,
    lat double precision not null,
    lng double precision not null,
    conAnillas boolean not null,
	cuantas integer not null,
    RT text,
    LB text,
    LT text,
    extraAnillas boolean not null,
    RM text,
    actividad text not null,
    lectura text not null,
    IP text not null,
    creado DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- Nidos
DROP TABLE IF EXISTS nidos;
CREATE TABLE nidos (
    id integer primary key autoincrement,
    usuarioId integer not null,
    lat double precision not null,
    lng double precision not null,
    IP text not null,
    creado DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- Dormideros
DROP TABLE IF EXISTS dormideros;
CREATE TABLE dormideros (
    id integer primary key autoincrement,
    usuarioId integer not null,
    lat double precision not null,
    lng double precision not null,
    IP text not null,
    creado DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- Datos
DROP TABLE IF EXISTS datos_urracas;
CREATE TABLE datos_urracas (
    id integer primary key autoincrement,
    -- DATOS de CAPTURA
    coordn double precision,
    coordw double precision,
    fecha text,
    lugar text,
    horaini text,
    metal text,
    idcolor integer,
    ds text,
    ii text,
    _is text,
    dm text,
    horacapt text,
    -- DATOS BIOMÉTRICOS
    edad double precision,
    sexo text,
    grasa double precision,
    musculo double precision,
    pesom boolean,
    peso double precision,
    placa double precision,
    tarsom boolean,
    tarso double precision,
    cpm boolean,
    cp double precision,
    pculmenm boolean,
    pculmen double precision,
    paltom boolean,
    palto double precision,
    panchom boolean,
    pancho double precision,
    alam boolean,
    ala double precision,
    pp1m boolean,
    pp1 double precision,
    pp2m boolean,
    pp2 double precision,
    pp3m boolean,
    pp3 double precision,
    pp4m boolean,
    pp4 double precision,
    pp5m boolean,
    pp5 double precision,
    pp6m boolean,
    pp6 double precision,
    pp7m boolean,
    pp7 double precision,
    pp8m boolean,
    pp8 double precision,
    pp9m boolean,
    pp9 double precision,
    pp10m boolean,
    pp10 double precision,
    negropp1m boolean,
    negropp1 double precision,
    negropp2m boolean,
    negropp2 double precision,
    colam boolean,
    cola double precision,
    -- DATOS MUESTRAS
    fotocara boolean,
    fotocaraid text,
    fototarso boolean,
    fototarsoid text,
    plumas boolean,
    plumasid text,
    sangre boolean,
    sangreid text,
    dieta boolean,
    dietaid text,
    mudaact boolean,
    mudaactid text,
    -- OTROS DATOS CAPTURA
    horafin text,
    comentarios text,
    usuario text
);

-- Apadrinamientos
DROP TABLE IF EXISTS apadrinamientos;
CREATE TABLE apadrinamientos (
    id integer primary key autoincrement,
    usuarioId integer not null,
    idcolor integer,
    nombre text,
    validado boolean default 0,
    IP text,
    creado DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- Relaciones parentesco
DROP TABLE IF EXISTS relaciones_parentesco;
CREATE TABLE relaciones_parentesco (
    id integer primary key autoincrement,
    usuarioId integer not null,
    metal_sujeto text not null,
    tipo_relacion integer not null,
    metal_objeto text not null,
    FOREIGN KEY(tipo_relacion) REFERENCES relaciones_parentesco_tipos(id)
);
DROP TABLE IF EXISTS relaciones_parentesco_tipos;
CREATE TABLE relaciones_parentesco_tipos (
    id integer primary key autoincrement,
    descripcion text
);
INSERT INTO relaciones_parentesco_tipos (descripcion) VALUES
    ('descendiente'),
    ('ascendiente'),
    ('pareja'),
    ('hermano')
;

-- Relaciones de lugar
