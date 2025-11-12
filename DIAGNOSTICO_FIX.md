DIAGNÓSTICO Y FIX - PROBLEMA DE PREDICCIÓN DE FRACTURAS
======================================================

PROBLEMA IDENTIFICADO:
- Las imágenes de huesos fracturados retornaban "normal" cuando debían retornar "fractured"

CAUSA RAÍZ:
La normalización de la imagen en `predictions.py` era incorrecta:

  INCORRECTO (línea anterior):
  x = x / 255.0  # Solo normaliza a [0, 1]

  CORRECTO (aplicado):
  x = tf.keras.applications.resnet50.preprocess_input(x)  # Normaliza a [-1, 1] con media ImageNet

EXPLICACIÓN TÉCNICA:
- En `training_fracture.py`, el modelo se entrenó usando:
  ```python
  preprocessing_function=tf.keras.applications.resnet50.preprocess_input
  ```
  Esta función aplica sustracción de media ImageNet, convirtiendo píxeles a rango [-1, 1]

- En `predictions.py`, se usaba división por 255.0 que solo normaliza a [0, 1]

- Esta discrepancia entre el rango de entrenamiento y el de predicción causaba que
  el modelo recibiera datos fuera del rango esperado, resultando en predicciones incorrectas

CAMBIOS REALIZADOS:
1. ✓ Archivo: predictions.py
   - Reemplazó: x = x / 255.0
   - Por: x = tf.keras.applications.resnet50.preprocess_input(x)

2. ✓ Archivo: app.py
   - Agregó logging para debugging
   - Agregó mejor manejo de excepciones
   - Agregó límite de tamaño de archivo (16MB)

VERIFICACIÓN:
Ahora el flujo de predicción es:
1. Cargar imagen → Convertir a array → Normalizar con preprocess_input
2. Predecir parte del cuerpo (Parts model)
3. Predecir estatus de fractura (modelo específico de la parte)
4. Retornar resultado ("fractured" o "normal")

MAPEO DE CATEGORÍAS:
- Fracturas: ["fractured" (idx 0), "normal" (idx 1)]
- Partes: ["Elbow" (idx 0), "Hand" (idx 1), "Shoulder" (idx 2)]

El mapeo es correcto porque Keras ordena alfabéticamente las clases en flow_from_dataframe
