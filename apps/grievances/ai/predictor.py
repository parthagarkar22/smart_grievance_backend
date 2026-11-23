


# import numpy as np
# from tensorflow.keras.preprocessing import image
# from .model_loader import model, INDEX_TO_CLASS


# print("✅ Predictor module loaded")


# def predict_image(img_path):
#     """
#     Predict grievance category from image
#     Returns: (predicted_label, confidence)
#     """

#     img = image.load_img(img_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = img_array / 255.0

#     preds = model.predict(img_array)

#     top_index = int(np.argmax(preds[0]))
#     confidence = float(preds[0][top_index])

#     predicted_label = INDEX_TO_CLASS[top_index]

#     print("🧠 AI Prediction:", predicted_label)
#     print("📊 Confidence:", confidence)

#     return predicted_label, confidence







# import numpy as np
# from tensorflow.keras.preprocessing import image
# from .model_loader import model, INDEX_TO_CLASS

# print("✅ Predictor module loaded")


# def predict_image(img_path, threshold=0.25):
#     """
#     Predict grievance categories from image (Multi-label)

#     Returns:
#     detected_labels (list)
#     max_confidence (float)
#     """

#     img = image.load_img(img_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)

#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = img_array / 255.0

#     preds = model.predict(img_array)[0]

#     detected_labels = []

#     # 🔍 Detect multiple problems
#     for i, prob in enumerate(preds):

#         if prob >= threshold:
#             label = INDEX_TO_CLASS[i]
#             detected_labels.append(label)

#     # fallback if nothing detected
#     if not detected_labels:
#         top_index = int(np.argmax(preds))
#         detected_labels.append(INDEX_TO_CLASS[top_index])

#     max_confidence = float(np.max(preds))

#     print("🧠 AI Predictions:", detected_labels)
#     print("📊 Max Confidence:", max_confidence)

#     return detected_labels, max_confidence





# from ultralytics import YOLO
# import os

# print("✅ YOLO Predictor module loaded")

# # -----------------------------------------------------
# # Load trained civic AI model
# # -----------------------------------------------------

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "civic_ai.pt")

# print("📦 Loading model from:", MODEL_PATH)

# model = YOLO(MODEL_PATH)


# # -----------------------------------------------------
# # Map detected objects → Departments
# # -----------------------------------------------------

# OBJECT_DEPARTMENT_MAP = {
#     "garbage": "garbage",
#     "road": "road",
#     "water": "water",
#     "sewage": "sewage",
#     "light": "light"
# }


# # -----------------------------------------------------
# # Prediction function
# # -----------------------------------------------------

# def predict_image(img_path):

#     results = model(img_path)

#     predictions = []

#     for r in results:

#         boxes = r.boxes
#         names = r.names

#         if boxes is None:
#             continue

#         for cls, conf in zip(boxes.cls, boxes.conf):

#             label = names[int(cls)].lower()
#             confidence = float(conf)

#             print("Detected:", label, "confidence:", confidence)

#             if label in OBJECT_DEPARTMENT_MAP:

#                 predictions.append({
#                     "department": OBJECT_DEPARTMENT_MAP[label],
#                     "confidence": confidence
#                 })

#     # sort predictions by confidence
#     predictions = sorted(predictions, key=lambda x: x["confidence"], reverse=True)

#     detected_departments = []
#     seen = set()

#     # allow multiple departments
#     for pred in predictions:

#         if pred["confidence"] >= 0.25 and pred["department"] not in seen:
#             detected_departments.append(pred["department"])
#             seen.add(pred["department"])

#         if len(detected_departments) == 3:
#             break

#     # fallback
#     if not detected_departments:
#         detected_departments.append("unknown")

#     print("🧠 AI Predictions:", detected_departments)

#     return detected_departments, 0.90

# from ultralytics import YOLO
# import os
# import cv2

# print("✅ YOLO Predictor module loaded")

# # -----------------------------------------------------
# # Load trained civic AI model
# # -----------------------------------------------------

# BASE_DIR = os.path.dirname(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.dirname(os.path.abspath(__file__))
#         )
#     )
# )

# MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "civic_ai.pt")

# print("📦 Loading model from:", MODEL_PATH)

# model = YOLO(MODEL_PATH)


# # -----------------------------------------------------
# # Map detected objects → Departments
# # -----------------------------------------------------

# OBJECT_DEPARTMENT_MAP = {
#     "garbage": "garbage",
#     "road": "road",
#     "water": "water",
#     "sewage": "sewage",
#     "light": "light"
# }


# # -----------------------------------------------------
# # Prediction function
# # -----------------------------------------------------

# def predict_image(img_path):

#     image = cv2.imread(img_path)

#     if image is None:
#         print("❌ Image not found:", img_path)
#         return ["unknown"], 0.0

#     height, width, _ = image.shape

#     detected_departments = set()

#     # -------------------------------------------------
#     # Split image into 4 tiles
#     # -------------------------------------------------

#     tiles = [
#         image[0:height//2, 0:width//2],       # top-left
#         image[0:height//2, width//2:width],   # top-right
#         image[height//2:height, 0:width//2],  # bottom-left
#         image[height//2:height, width//2:width]  # bottom-right
#     ]

#     # -------------------------------------------------
#     # Run YOLO detection on each tile
#     # -------------------------------------------------

#     for tile in tiles:

#         results = model(tile, conf=0.25)

#         for r in results:

#             if r.boxes is None:
#                 continue

#             for cls, conf in zip(r.boxes.cls, r.boxes.conf):

#                 label = r.names[int(cls)].lower()
#                 confidence = float(conf)

#                 print("Detected:", label, "confidence:", confidence)

#                 if label in OBJECT_DEPARTMENT_MAP:
#                     detected_departments.add(
#                         OBJECT_DEPARTMENT_MAP[label]
#                     )

#     # -------------------------------------------------
#     # Fallback if nothing detected
#     # -------------------------------------------------

#     if not detected_departments:
#         detected_departments.add("unknown")

#     detected_departments = list(detected_departments)

#     print("🧠 AI Predictions:", detected_departments)

#     return detected_departments, 0.90

from ultralytics import YOLO
import os

print("✅ YOLO Predictor module loaded")

# -----------------------------------------------------
# Load trained civic AI model
# -----------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "civic_ai.pt")

print("📦 Loading model from:", MODEL_PATH)

model = YOLO(MODEL_PATH)

# class names directly from the model
CLASS_NAMES = model.names


# -----------------------------------------------------
# Map detected objects → Departments
# -----------------------------------------------------

OBJECT_DEPARTMENT_MAP = {
    "garbage": "garbage",
    "road": "road",
    "water": "water",
    "sewage": "sewage",
    "light": "light"
}


# -----------------------------------------------------
# Prediction function
# -----------------------------------------------------

def predict_image(img_path):

    results = model(img_path)

    detected_departments = set()

    for r in results:

        if r.boxes is None:
            continue

        for cls, conf in zip(r.boxes.cls, r.boxes.conf):

            confidence = float(conf)

            # ignore weak detections
            if confidence < 0.3:
                continue

            label = CLASS_NAMES[int(cls)].lower()

            print("RAW LABEL:", label)
            print("Confidence:", confidence)

            if label in OBJECT_DEPARTMENT_MAP:
                detected_departments.add(
                    OBJECT_DEPARTMENT_MAP[label]
                )

    # fallback
    if not detected_departments:
        detected_departments.add("unknown")

    detected_departments = list(detected_departments)

    print("🧠 FINAL AI Predictions:", detected_departments)

    return detected_departments, 0.9
