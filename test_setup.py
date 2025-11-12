"""
Script para pruebas rápidas del flujo de predicción
Ejecutar: python test_prediction_quick.py
"""

import os
import sys

# Verificar que existen los archivos necesarios
test_dir = "test"
elbow_fractured = os.path.join(test_dir, "Elbow", "fractured")
elbow_normal = os.path.join(test_dir, "Elbow", "normal")

print("="*70)
print("VERIFICACIÓN DE ARCHIVOS DE TEST")
print("="*70)

if os.path.exists(elbow_fractured):
    files = [f for f in os.listdir(elbow_fractured) if f.endswith(('.jpg', '.jpeg', '.png'))]
    print(f"✓ Carpeta 'fractured' encontrada: {len(files)} imágenes")
    if files:
        print(f"  Ejemplo: {files[0]}")
else:
    print(f"✗ Carpeta no encontrada: {elbow_fractured}")

if os.path.exists(elbow_normal):
    files = [f for f in os.listdir(elbow_normal) if f.endswith(('.jpg', '.jpeg', '.png'))]
    print(f"✓ Carpeta 'normal' encontrada: {len(files)} imágenes")
    if files:
        print(f"  Ejemplo: {files[0]}")
else:
    print(f"✗ Carpeta no encontrada: {elbow_normal}")

print("\n" + "="*70)
print("VERIFICACIÓN DE MODELOS")
print("="*70)

weights_dir = "weights"
models = [
    "ResNet50_BodyParts.h5",
    "ResNet50_Elbow_frac.h5",
    "ResNet50_Hand_frac.h5",
    "ResNet50_Shoulder_frac.h5"
]

for model in models:
    path = os.path.join(weights_dir, model)
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / (1024*1024)
        print(f"✓ {model}: {size_mb:.2f} MB")
    else:
        print(f"✗ {model}: NO ENCONTRADO")

print("\n" + "="*70)
print("VERIFICACIÓN DE DEPENDENCIAS")
print("="*70)

dependencies = [
    ("tensorflow", "TensorFlow"),
    ("keras", "Keras"),
    ("numpy", "NumPy"),
    ("pandas", "Pandas"),
    ("sklearn", "scikit-learn"),
]

for module, name in dependencies:
    try:
        __import__(module)
        print(f"✓ {name} instalado")
    except ImportError:
        print(f"✗ {name} NO instalado")

print("\n" + "="*70)
print("PRÓXIMOS PASOS")
print("="*70)
print("1. Instala dependencias: pip install -r requirements.txt")
print("2. Prueba con: python debug_predictions.py")
print("3. O inicia el servidor: python app.py")
print("="*70)
