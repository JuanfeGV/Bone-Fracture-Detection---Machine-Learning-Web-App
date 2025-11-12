import os
import sys
import numpy as np
import tensorflow as tf
from keras.preprocessing import image

# Carga de modelos con manejo de errores
print("Loading models...")
try:
    model_elbow_frac = tf.keras.models.load_model("weights/ResNet50_Elbow_frac.h5")
    print("✓ Elbow model loaded")
except Exception as e:
    print(f"✗ Error loading Elbow model: {e}")
    model_elbow_frac = None

try:
    model_parts = tf.keras.models.load_model("weights/ResNet50_BodyParts.h5")
    print("✓ Parts model loaded")
except Exception as e:
    print(f"✗ Error loading Parts model: {e}")
    model_parts = None

categories_parts = ["Elbow", "Hand", "Shoulder"]
categories_fracture = ["fractured", "normal"]

def test_predict(img_path, model_name="Parts"):
    size = 224
    
    if model_name == "Parts":
        chosen_model = model_parts
    elif model_name == "Elbow":
        chosen_model = model_elbow_frac
    else:
        return None
    
    if chosen_model is None:
        return "MODEL_NOT_LOADED"
    
    try:
        temp_img = image.load_img(img_path, target_size=(size, size))
        x = image.img_to_array(temp_img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0
        
        pred = chosen_model.predict(x, verbose=0)
        prediction_idx = np.argmax(pred, axis=1)[0]
        prediction_conf = pred[0][prediction_idx]
        
        if model_name == "Parts":
            prediction_str = categories_parts[prediction_idx]
        else:
            prediction_str = categories_fracture[prediction_idx]
        
        return prediction_str, prediction_idx, prediction_conf
    except Exception as e:
        return f"ERROR: {e}"

print("\n" + "="*60)
print("Testing with FRACTURED images:")
print("="*60)

fractured_path = 'test/Elbow/fractured/broken_elbow.jpeg'
if os.path.exists(fractured_path):
    result = test_predict(fractured_path, model_name="Elbow")
    print(f"Image: {fractured_path}")
    if isinstance(result, tuple):
        print(f"  Prediction: {result[0]}")
        print(f"  Index: {result[1]}")
        print(f"  Confidence: {result[2]:.4f}")
    else:
        print(f"  Result: {result}")

print("\n" + "="*60)
print("Testing with NORMAL images:")
print("="*60)

normal_path = 'test/Elbow/normal/elbow1.jpeg'
if os.path.exists(normal_path):
    result = test_predict(normal_path, model_name="Elbow")
    print(f"Image: {normal_path}")
    if isinstance(result, tuple):
        print(f"  Prediction: {result[0]}")
        print(f"  Index: {result[1]}")
        print(f"  Confidence: {result[2]:.4f}")
    else:
        print(f"  Result: {result}")

print("\n" + "="*60)
print("Categories mapping:")
print("="*60)
print(f"Fracture categories: {categories_fracture}")
print(f"  Index 0 -> '{categories_fracture[0]}'")
print(f"  Index 1 -> '{categories_fracture[1]}'")
