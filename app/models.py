from app import db
from flask import flash, url_for, redirect
from datetime import datetime
from flask_login import UserMixin, LoginManager, current_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import json

login_manager = LoginManager()
login_manager.login_view = 'login'  

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash('Acceso denegado. Se requieren privilegios de administrador.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def create_admin():
    admin = Usuario.query.filter_by(rol='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            email='admin@liceo.com',
            rol='admin'
        )
        admin.set_password('admin123')  # Cambiar en producción
        db.session.add(admin)
        db.session.commit()

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
    categoria = db.Column(db.String(50), nullable = True, default = 'general')  # Nuevo campo
    imagen_url = db.Column(db.String(200), nullable = True)  # Nuevo campo
    _archivos_urls = db.Column(db.Text, nullable = True, default = '[]')  # Nuevo campo para archivos adjuntos
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_expiracion = db.Column(db.DateTime, nullable=True)
    
    # Clave foránea para el usuario
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Estado de la noticia
    activa = db.Column(db.Boolean, default=True)
    
    # Relación con archivos adjuntos
    archivos = db.relationship('ArchivoAdjunto', backref='noticia', lazy=True)
    
    @property
    def archivos_urls(self):
        return json.loads(self._archivos_urls) if self._archivos_urls else []

    @archivos_urls.setter
    def archivos_urls(self, urls):
        self._archivos_urls = json.dumps(urls) if urls else '[]'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'contenido': self.contenido,
            'categoria': self.categoria,
            'imagen_url': self.imagen_url,
            'archivos_urls': self.archivos_urls,
            'fecha_publicacion': self.fecha_publicacion.isoformat(),
            'autor_id': self.autor_id
        }

class ArchivoAdjunto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ruta = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'imagen', 'pdf', etc.
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clave foránea para la noticia
    noticia_id = db.Column(db.Integer, db.ForeignKey('noticia.id'), nullable=False)