import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "grievance_classifier.h5")
CLASS_INDEX_PATH = os.path.join(BASE_DIR, "ai_models", "class_indices.json")

_model = None
CLASS_TO_INDEX = {}
INDEX_TO_CLASS = {}


def get_model():
    """Lazy-load TensorFlow model so app boot/migrate does not require TF init."""
    global _model, CLASS_TO_INDEX, INDEX_TO_CLASS
    if _model is None:
        import tensorflow as tf
        _model = tf.keras.models.load_model(MODEL_PATH)
        with open(CLASS_INDEX_PATH, "r") as f:
            CLASS_TO_INDEX = json.load(f)
        INDEX_TO_CLASS = {v: k for k, v in CLASS_TO_INDEX.items()}
        print("✅ AI Model Loaded")
    return _model


# Backwards-compatible aliases used by older imports
def __getattr__(name):
    if name == "model":
        return get_model()
    if name in ("CLASS_TO_INDEX", "INDEX_TO_CLASS"):
        get_model()
        return globals()[name]
    raise AttributeError(name)
