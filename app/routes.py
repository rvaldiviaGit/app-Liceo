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
    
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db
from app.models import Noticia, Usuario
from werkzeug.security import generate_password_hash

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
def crear_noticia():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        
        nueva_noticia = Noticia(
            titulo=titulo, 
            contenido=contenido, 
            autor=current_user
        )
        
        db.session.add(nueva_noticia)
        db.session.commit()
        
        flash('Noticia creada exitosamente', 'success')
        return redirect(url_for('index'))
    
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
