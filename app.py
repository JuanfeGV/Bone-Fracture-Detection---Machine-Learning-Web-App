from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from predictions import predict
import tensorflow as tf
import numpy as np

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura_123'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/predict', methods=['GET', 'POST'])
def upload_predict():
    if 'username' not in session:
        flash('Debe iniciar sesión para acceder al análisis.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se ha subido ninguna imagen.', 'danger')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('Seleccione una imagen válida.', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            bone_type = predict(filepath, "Parts")  # Paso 1: detectar parte del cuerpo
            fracture_status = predict(filepath, bone_type)  # Paso 2: usar modelo correcto

            return render_template(
                'predict.html',
                filename=filename,
                bone_type=bone_type,
                result=fracture_status
            )
    return render_template('predict.html')

@app.route('/uploads/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
