from apps.grievances.models import Grievance
# from apps.grievances.utils.similarity import cosine_sim, get_distance
from apps.grievances.utils import cosine_sim, get_distance


# ======================================================
# 🔧 THRESHOLDS (TUNE THESE)
# ======================================================

TEXT_THRESHOLD = 0.8
IMAGE_THRESHOLD = 0.9
DISTANCE_THRESHOLD = 0.1  # in KM (0.1 = 100 meters)


# ======================================================
# 🧠 MAIN DUPLICATE DETECTION FUNCTION
# ======================================================

def find_duplicate(new_obj):
    """
    Finds duplicate complaint based on:
    - Text similarity
    - Image similarity
    - Location distance
    """

    # Only check MAIN complaints (not duplicates)
    # existing_complaints = Grievance.objects.filter(is_duplicate=False)
    existing_complaints = Grievance.objects.filter(
    is_duplicate=False
    ).exclude(id=new_obj.id)

    for comp in existing_complaints:

        # -----------------------------
        # 📍 LOCATION CHECK
        # -----------------------------
        distance = get_distance(
            new_obj.location.y,
            new_obj.location.x,
            comp.location.y,
            comp.location.x
        )

        # Skip if far away
        if distance > DISTANCE_THRESHOLD:
            continue

        # -----------------------------
        # 🧠 TEXT SIMILARITY
        # -----------------------------
        text_score = 0

        if comp.text_embedding and new_obj.text_embedding:
            text_score = cosine_sim(
                comp.text_embedding,
                new_obj.text_embedding
            )

        # -----------------------------
        # 🖼️ IMAGE SIMILARITY
        # -----------------------------
        image_score = 0

        if comp.image_embedding and new_obj.image_embedding:
            image_score = cosine_sim(
                comp.image_embedding,
                new_obj.image_embedding
            )

        # -----------------------------
        # 🧠 DEBUG (REMOVE IN PROD)
        # -----------------------------
        print("----- DUPLICATE CHECK -----")
        print(f"Comparing with ID: {comp.id}")
        print(f"Distance: {distance}")
        print(f"Text Score: {text_score}")
        print(f"Image Score: {image_score}")

        # -----------------------------
        # 🔥 FINAL DECISION
        # -----------------------------
        if (
            text_score >= TEXT_THRESHOLD
            or image_score >= IMAGE_THRESHOLD
        ):
            print("✅ DUPLICATE FOUND\n")
            return comp

    # -----------------------------
    # ❌ NO DUPLICATE
    # -----------------------------
    print("❌ NO DUPLICATE FOUND\n")
    return None