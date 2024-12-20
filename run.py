""" from app import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True) """
    
""" from app import app, db

if __name__ == '__main__':
    # Crear la base de datos si no existe
    with app.app_context():
        db.create_all()
    
    # Ejecutar la aplicación
    app.run(debug=True) """
    
from app import app, db
from app.models import Usuario, Noticia, ArchivoAdjunto

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)