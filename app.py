from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import logging
from werkzeug.utils import secure_filename
from predictions import predict

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura_123'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

USER = {
    "username": "admin",
    "password": "fractura123"
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('menu'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER["username"] and password == USER["password"]:
            session['username'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/menu')
def menu():
    if 'username' not in session:
        flash('Debe iniciar sesión para acceder al menú.', 'warning')
        return redirect(url_for('login'))
    return render_template('menu.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/analisis', methods=['GET'])
def analisis():
    if 'username' not in session:
        flash('Debe iniciar sesión para acceder al análisis.', 'warning')
        return redirect(url_for('login'))
    return render_template('analisis.html')

@app.route('/analizar_imagen', methods=['POST'])
def analizar_imagen():
    if 'username' not in session:
        flash('Debe iniciar sesión para acceder al análisis.', 'warning')
        return redirect(url_for('login'))

    if 'imagen' not in request.files:
        flash('No se ha subido ninguna imagen.', 'danger')
        return redirect(request.url)

    imagen = request.files['imagen']

    if imagen.filename == '':
        flash('Seleccione una imagen válida.', 'danger')
        return redirect(request.url)

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        imagen.save(filepath)

        try:
            logger.info(f"Processing image: {filepath}")
            # Primero detectar la parte del cuerpo (Elbow, Hand, Shoulder)
            body_part = predict(filepath, model="Parts")
            logger.info(f"Detected body part: {body_part}")
            # Luego usar el modelo específico para detectar fractura en esa parte
            fracture_status = predict(filepath, model=body_part)
            logger.info(f"Fracture status: {fracture_status}")
        except Exception as e:
            logger.error(f"Error al predecir: {e}", exc_info=True)
            flash('Error al analizar la imagen. Verifica que sea una imagen válida.', 'danger')
            return redirect(url_for('analisis'))

        # fracture_status contiene 'fractured' o 'normal'
        return render_template('analisis.html', resultado=fracture_status, filename=filename, body_part=body_part)

    flash('Formato de archivo no permitido. Solo PNG, JPG o JPEG.', 'danger')
    return redirect(url_for('analisis'))

@app.route('/uploads/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
