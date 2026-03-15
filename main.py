import os
import sys
import json
import joblib
import numpy as np

# 1. FIX THE IMPORTS FOR LIGHTWEIGHT RUNTIME
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    from tensorflow import lite as tflite

# 2. DEBUG: PRINT EVERYTHING
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"--- RENDER DEBUG ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"Base Directory: {BASE_DIR}")
print(f"Files in directory: {os.listdir(BASE_DIR)}")

def load_file(name):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        print(f"❌ CRITICAL MISSING FILE: {name} at {path}")
        return None
    return path

# 3. SECURE LOADING
try:
    # Check filenames - names MUST match your GitHub exactly (Case Sensitive)
    tflite_path = load_file("model_optimized.tflite")
    best_model_path = load_file("best_model.pkl")
    scaler_path = load_file("scaler.pkl")
    label_encoder_path = load_file("label_encoder.pkl")
    labels_json_path = load_file("disease_labels.json")

    if None in [tflite_path, best_model_path, scaler_path, label_encoder_path, labels_json_path]:
        print("❌ App cannot start due to missing files.")
        sys.exit(1)

    # Initialize TFLite
    interpreter = tflite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    
    # Load Pickles
    model = joblib.load(best_model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(label_encoder_path)
    
    with open(labels_json_path, "r") as f:
        disease_labels = json.load(f)

    print("✅ ALL MODELS LOADED SUCCESSFULLY")

except Exception as e:
    print(f"❌ STARTUP ERROR: {str(e)}")
    sys.exit(1)
