# def final_department_decision(text_dept: str, image_dept: str) -> str:
#     """
#     Decide final department based on both text and image prediction
#     """

#     # Case 1: Both match → perfect
#     if text_dept == image_dept:
#         return text_dept

#     # Case 2: Image is more reliable → prefer image
#     if image_dept and image_dept != "General":
#         return image_dept

#     # Case 3: Otherwise fallback to text
#     return text_dept or "General"

# def detect_department(text: str) -> str:

#     if not text:
#         return "General"

#     text = text.lower()

#     WATER_KEYWORDS = ["water", "pipe", "leak", "leakage", "tap", "supply"]
#     ROAD_KEYWORDS = ["road", "pothole", "street", "bridge", "footpath"]
#     LIGHT_KEYWORDS = ["light", "electric", "electricity", "lamp", "street light", "power"]
#     SEWAGE_KEYWORDS = ["sewage", "drain", "gutter", "manhole", "overflow"]
#     GARBAGE_KEYWORDS = ["garbage", "waste", "trash", "dump", "dirty", "cleaning"]

#     for word in WATER_KEYWORDS:
#         if word in text:
#             return "Water"

#     for word in ROAD_KEYWORDS:
#         if word in text:
#             return "Road"

#     for word in LIGHT_KEYWORDS:
#         if word in text:
#             return "Light"

#     for word in SEWAGE_KEYWORDS:
#         if word in text:
#             return "Sewage"

#     for word in GARBAGE_KEYWORDS:
#         if word in text:
#             return "Garbage"

#     return "General"


# def detect_priority(text: str) -> str:

#     if not text:
#         return "LOW"

#     text = text.lower()

#     CRITICAL_KEYWORDS = ["accident", "fire", "burst", "explosion",
#                          "collapsed", "dead", "danger", "emergency"]

#     HIGH_KEYWORDS = ["leakage", "overflow", "not working",
#                      "severe", "blocked", "huge", "broken"]

#     MEDIUM_KEYWORDS = ["delay", "slow", "issue", "problem",
#                        "repair", "damage"]

#     for word in CRITICAL_KEYWORDS:
#         if word in text:
#             return "CRITICAL"

#     for word in HIGH_KEYWORDS:
#         if word in text:
#             return "HIGH"

#     for word in MEDIUM_KEYWORDS:
#         if word in text:
#             return "MEDIUM"

#     return "LOW"


# from typing import List

# # -----------------------------------------------------
# # FINAL DEPARTMENT DECISION (MULTI DEPARTMENT SUPPORT)
# # -----------------------------------------------------

# def final_department_decision(text_depts: List[str], image_depts: List[str]) -> List[str]:
#     """
#     Decide final departments based on both text and image prediction.

#     Priority:
#     1️⃣ Image detection (highest priority)
#     2️⃣ Text detection (secondary)
#     3️⃣ Fallback to General
#     """

#     # Remove "General" if present
#     text_depts = [d for d in text_depts if d != "General"]
#     image_depts = [d for d in image_depts if d != "General"]

#     # Case 1: Image detected departments → prefer image
#     if image_depts:
#         final_depts = set(image_depts)

#         # Allow text to support only if related
#         for dept in text_depts:
#             if dept in image_depts:
#                 final_depts.add(dept)

#         return list(final_depts)

#     # Case 2: Image failed → fallback to text
#     if text_depts:
#         return list(set(text_depts))

#     # Case 3: Nothing detected
#     return ["General"]


# # -----------------------------------------------------
# # TEXT BASED DEPARTMENT DETECTION (MULTI)
# # -----------------------------------------------------

# def detect_department(text: str) -> List[str]:

#     if not text:
#         return ["General"]

#     text = text.lower()

#     WATER_KEYWORDS = [
#         "water", "pipe", "leak", "leakage",
#         "tap", "supply"
#     ]

#     ROAD_KEYWORDS = [
#         "road", "pothole", "street",
#         "bridge", "footpath"
#     ]

#     LIGHT_KEYWORDS = [
#         "light", "electric", "electricity",
#         "lamp", "street light", "power"
#     ]

#     SEWAGE_KEYWORDS = [
#         "sewage", "drain", "gutter",
#         "manhole", "overflow"
#     ]

#     GARBAGE_KEYWORDS = [
#         "garbage", "waste", "trash",
#         "dump", "dirty", "cleaning"
#     ]

#     detected = set()

#     for word in WATER_KEYWORDS:
#         if word in text:
#             detected.add("Water")

#     for word in ROAD_KEYWORDS:
#         if word in text:
#             detected.add("Road")

#     for word in LIGHT_KEYWORDS:
#         if word in text:
#             detected.add("Light")

#     for word in SEWAGE_KEYWORDS:
#         if word in text:
#             detected.add("Sewage")

#     for word in GARBAGE_KEYWORDS:
#         if word in text:
#             detected.add("Garbage")

#     if not detected:
#         return ["General"]

#     return list(detected)


# # -----------------------------------------------------
# # PRIORITY DETECTION
# # -----------------------------------------------------

# def detect_priority(text: str) -> str:

#     if not text:
#         return "LOW"

#     text = text.lower()

#     CRITICAL_KEYWORDS = [
#         "accident", "fire", "burst",
#         "explosion", "collapsed",
#         "dead", "danger", "emergency"
#     ]

#     HIGH_KEYWORDS = [
#         "leakage", "overflow",
#         "not working", "severe",
#         "blocked", "huge", "broken"
#     ]

#     MEDIUM_KEYWORDS = [
#         "delay", "slow",
#         "issue", "problem",
#         "repair", "damage"
#     ]

#     for word in CRITICAL_KEYWORDS:
#         if word in text:
#             return "CRITICAL"

#     for word in HIGH_KEYWORDS:
#         if word in text:
#             return "HIGH"

#     for word in MEDIUM_KEYWORDS:
#         if word in text:
#             return "MEDIUM"

#     return "LOW"


from typing import List

# -----------------------------------------------------
# FINAL DEPARTMENT DECISION (MULTI DEPARTMENT SUPPORT)
# -----------------------------------------------------

def final_department_decision(text_depts: List[str], image_depts: List[str]) -> List[str]:
    """
    Decide final departments based on both text and image prediction.

    Logic:
    1️⃣ Always trust image detections
    2️⃣ Allow text to add additional departments
    3️⃣ Remove duplicates
    4️⃣ Limit to max 3 departments
    """

    # Remove "General"
    text_depts = [d for d in text_depts if d != "General"]
    image_depts = [d for d in image_depts if d != "General"]

    final_depts = set()

    # 1️⃣ Always include image detections
    if image_depts:
        final_depts.update(image_depts)

    # 2️⃣ Allow text detection to add additional departments
    if text_depts:
        final_depts.update(text_depts)

    # 3️⃣ If nothing detected
    if not final_depts:
        return ["General"]

    # 4️⃣ Limit departments (avoid noisy AI predictions)
    return list(final_depts)[:3]


# -----------------------------------------------------
# TEXT BASED DEPARTMENT DETECTION (MULTI)
# -----------------------------------------------------

def detect_department(text: str) -> List[str]:

    if not text:
        return ["General"]

    text = text.lower()

    WATER_KEYWORDS = [
        "water", "pipe", "leak", "leakage",
        "tap", "supply"
    ]

    ROAD_KEYWORDS = [
        "road", "pothole", "street",
        "bridge", "footpath", "broken road"
    ]

    LIGHT_KEYWORDS = [
        "light", "electric", "electricity",
        "lamp", "street light", "power"
    ]

    SEWAGE_KEYWORDS = [
        "sewage", "drain", "gutter",
        "manhole", "overflow"
    ]

    GARBAGE_KEYWORDS = [
        "garbage", "waste", "trash",
        "dump", "dirty", "cleaning"
    ]

    detected = set()

    for word in WATER_KEYWORDS:
        if word in text:
            detected.add("Water")

    for word in ROAD_KEYWORDS:
        if word in text:
            detected.add("Road")

    for word in LIGHT_KEYWORDS:
        if word in text:
            detected.add("Light")

    for word in SEWAGE_KEYWORDS:
        if word in text:
            detected.add("Sewage")

    for word in GARBAGE_KEYWORDS:
        if word in text:
            detected.add("Garbage")

    if not detected:
        return ["General"]

    return list(detected)


# -----------------------------------------------------
# PRIORITY DETECTION
# -----------------------------------------------------

def detect_priority(text: str) -> str:

    if not text:
        return "LOW"

    text = text.lower()

    CRITICAL_KEYWORDS = [
        "accident", "fire", "burst",
        "explosion", "collapsed",
        "dead", "danger", "emergency"
    ]

    HIGH_KEYWORDS = [
        "leakage", "overflow",
        "not working", "severe",
        "blocked", "huge", "broken"
    ]

    MEDIUM_KEYWORDS = [
        "delay", "slow",
        "issue", "problem",
        "repair", "damage"
    ]

    for word in CRITICAL_KEYWORDS:
        if word in text:
            return "CRITICAL"

    for word in HIGH_KEYWORDS:
        if word in text:
            return "HIGH"

    for word in MEDIUM_KEYWORDS:
        if word in text:
            return "MEDIUM"

    return "LOW"