


import numpy as np
from tensorflow.keras.preprocessing import image
from .model_loader import model, INDEX_TO_CLASS


print("✅ Predictor module loaded")


def predict_image(img_path):
    """
    Predict grievance category from image
    Returns: (predicted_label, confidence)
    """

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    preds = model.predict(img_array)

    top_index = int(np.argmax(preds[0]))
    confidence = float(preds[0][top_index])

    predicted_label = INDEX_TO_CLASS[top_index]

    print("🧠 AI Prediction:", predicted_label)
    print("📊 Confidence:", confidence)

    return predicted_label, confidence
