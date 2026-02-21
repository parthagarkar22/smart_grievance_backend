import json
import os
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "grievance_classifier.h5")
CLASS_INDEX_PATH = os.path.join(BASE_DIR, "ai_models", "class_indices.json")

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_INDEX_PATH, "r") as f:
    CLASS_TO_INDEX = json.load(f)

INDEX_TO_CLASS = {v: k for k, v in CLASS_TO_INDEX.items()}

print("✅ AI Model Loaded")
