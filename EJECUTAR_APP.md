CÓMO EJECUTAR LA APLICACIÓN (POST-FIX)
======================================

PROBLEMA SOLUCIONADO:
Las imágenes fracturadas ahora se detectarán correctamente como "fractured"
en lugar de "normal".

Causa: La normalización de la imagen en predictions.py no coincidía con
la normalización usada en entrenamiento.

INSTRUCCIONES DE EJECUCIÓN:

1. Abre PowerShell y navega a la carpeta del proyecto:
   ```
   cd "c:\Users\felip\Documents\Universidad\6\Machine Learning\GitHub\Bone-Fracture-Detection---Machine-Learning-Web-App"
   ```

2. Instala las dependencias (si no las has instalado):
   ```
   pip install -r requirements.txt
   ```
   
   Esto instalará:
   - numpy
   - tensorflow
   - keras
   - pandas
   - matplotlib
   - scikit-learn
   - flask
   - colorama
   - pillow

3. Inicia la aplicación:
   ```
   python app.py
   ```

4. Abre tu navegador y ve a:
   ```
   http://127.0.0.1:5000
   ```

5. Inicia sesión con las credenciales de prueba:
   - Usuario: admin
   - Contraseña: fractura123

6. Navega a "Análisis de imágenes" y carga una imagen de prueba:
   - Usa imágenes de test/Elbow/fractured/ para probar fracturas
   - Usa imágenes de test/Elbow/normal/ para probar casos normales

CAMBIOS REALIZADOS:

✓ predictions.py:
  - Cambió normalización de "x / 255.0" a "tf.keras.applications.resnet50.preprocess_input(x)"
  - Esto asegura que la imagen se normaliza exactamente como se hizo en entrenamiento

✓ app.py:
  - Agregó logging para debugging
  - Agregó mejor manejo de excepciones
  - Agregó límite de tamaño de archivo (16MB)

✓ templates y style.css:
  - Diseño minimalista blanco/negro modo oscuro
  - Sidebar con menú desplegable
  - Advertencia visible sobre límites del modelo
  - Preview de imagen y resultado traducido

EXPECTED OUTPUT DESPUÉS DEL FIX:

Imagen: test/Elbow/fractured/broken_elbow.jpeg
→ Predicción esperada: "fractured" (ahora correcta)

Imagen: test/Elbow/normal/elbow1.jpeg
→ Predicción esperada: "normal" (sin cambios)

Si aún reciben predicciones incorrectas:
1. Revisa los logs en la consola de Flask para errores
2. Verifica que los modelos (.h5) estén en weights/
3. Asegúrate de que las dependencias estén correctamente instaladas
4. Prueba con: python debug_predictions.py (después de instalar deps)

ARCHIVOS MODIFICADOS:
- app.py
- predictions.py
- templates/login.html
- templates/menu.html
- templates/analisis.html
- static/style.css

ARCHIVOS NUEVOS:
- debug_predictions.py (para testing)
- test_setup.py (verificación de setup)
- DIAGNOSTICO_FIX.md (este documento - explicación técnica)
