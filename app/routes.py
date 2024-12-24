""" from flask import render_template
from app import app, db
from app.models import Noticia

@app.route('/')
def index():
    noticias = Noticia.query.order_by(Noticia.fecha_publicacion.desc()).all()
    return render_template('index.html', noticias=noticias) """

""" from flask import render_template
from app import app

@app.route('/')
def index():
    return "Prueba de funcionamiento!" """
    
from flask import render_template, flash, redirect,  url_for, request, jsonify
from flask_login import login_required, admin_required, current_user, login_user, logout_user
from app import app, db
from app.models import Noticia, Usuario
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os

#este comentario es solo para que pueda actualizar el local

# Configuración para subida de archivos
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS



@app.route('/')
def index():
    # Obtener las últimas noticias, ordenadas por fecha de publicación
    noticias = Noticia.query.order_by(Noticia.fecha_publicacion.desc()).limit(10).all()
    return render_template('index.html', noticias=noticias)

@app.route('/noticia/<int:noticia_id>')
def ver_noticia(noticia_id):
    noticia = Noticia.query.get_or_404(noticia_id)
    return render_template('noticia.html', noticia=noticia)

@app.route('/admin/crear_noticia', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_noticia():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            contenido = request.form['contenido']
            categoria = request.form['categoria']

            # Procesar imagen principal
            imagen_url = None
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen and allowed_image(imagen.filename):
                    filename = secure_filename(imagen.filename)
                    # Asegurarse de que el directorio existe
                    os.makedirs(os.path.join(app.static_folder, 'uploads', 'images'), exist_ok=True)
                    filepath = os.path.join(app.static_folder, 'uploads', 'images', filename)
                    imagen.save(filepath)
                    imagen_url = url_for('static', filename=f'uploads/images/{filename}')

            # Procesar archivos adjuntos
            archivos_urls = []
            if 'archivos' in request.files:
                archivos = request.files.getlist('archivos')
                for archivo in archivos:
                    if archivo and allowed_file(archivo.filename):
                        filename = secure_filename(archivo.filename)
                        # Asegurarse de que el directorio existe
                        os.makedirs(os.path.join(app.static_folder, 'uploads', 'files'), exist_ok=True)
                        filepath = os.path.join(app.static_folder, 'uploads', 'files', filename)
                        archivo.save(filepath)
                        archivos_urls.append(url_for('static', filename=f'uploads/files/{filename}'))

            nueva_noticia = Noticia(
                titulo=titulo,
                contenido=contenido,
                categoria=categoria,
                imagen_url=imagen_url,
                archivos_urls=archivos_urls,
                autor=current_user
            )

            db.session.add(nueva_noticia)
            db.session.commit()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'redirect': url_for('ver_noticia', noticia_id=nueva_noticia.id)
                })

            flash('Noticia creada exitosamente', 'success')
            return redirect(url_for('ver_noticia', noticia_id=nueva_noticia.id))

        except Exception as e:
            db.session.rollback()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': str(e)}), 500
            
            flash(f'Error al crear la noticia: {str(e)}', 'error')
            return redirect(url_for('crear_noticia'))

    return render_template('crear_noticia.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(username=username).first()
        if usuario_existente:
            flash('Nombre de usuario ya existe', 'error')
            return redirect(url_for('registro'))
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=username, 
            email=email,
            rol='editor'
        )
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        
        flash('Credenciales inválidas', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('index'))
