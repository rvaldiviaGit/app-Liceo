""" from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@localhost/liceo_blog'
db = SQLAlchemy(app) """


""" from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
# Por ahora, usaremos una base de datos SQLite simple
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liceo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes """


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liceo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configuración para uploads
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

db = SQLAlchemy(app)

migrate = Migrate(app, db)  # Añadimos esta línea

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app.models import Usuario, create_admin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

from app import routes

def init_app():
    login_manager.init_app(app)
    create_admin()