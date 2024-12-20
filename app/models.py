from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    rol = db.Column(db.String(20), nullable=False, default='editor')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con noticias
    noticias = db.relationship('Noticia', backref='autor', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_expiracion = db.Column(db.DateTime, nullable=True)
    
    # Clave foránea para el usuario
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Estado de la noticia
    activa = db.Column(db.Boolean, default=True)
    categoria = db.Column(db.String(50))
    
    # Relación con archivos adjuntos
    archivos = db.relationship('ArchivoAdjunto', backref='noticia', lazy=True)

class ArchivoAdjunto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ruta = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'imagen', 'pdf', etc.
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clave foránea para la noticia
    noticia_id = db.Column(db.Integer, db.ForeignKey('noticia.id'), nullable=False)