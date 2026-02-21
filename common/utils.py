def final_department_decision(text_dept: str, image_dept: str) -> str:
    """
    Decide final department based on both text and image prediction
    """

    # Case 1: Both match → perfect
    if text_dept == image_dept:
        return text_dept

    # Case 2: Image is more reliable → prefer image
    if image_dept and image_dept != "General":
        return image_dept

    # Case 3: Otherwise fallback to text
    return text_dept or "General"

def detect_department(text: str) -> str:

    if not text:
        return "General"

    text = text.lower()

    WATER_KEYWORDS = ["water", "pipe", "leak", "leakage", "tap", "supply"]
    ROAD_KEYWORDS = ["road", "pothole", "street", "bridge", "footpath"]
    LIGHT_KEYWORDS = ["light", "electric", "electricity", "lamp", "street light", "power"]
    SEWAGE_KEYWORDS = ["sewage", "drain", "gutter", "manhole", "overflow"]
    GARBAGE_KEYWORDS = ["garbage", "waste", "trash", "dump", "dirty", "cleaning"]

    for word in WATER_KEYWORDS:
        if word in text:
            return "Water"

    for word in ROAD_KEYWORDS:
        if word in text:
            return "Road"

    for word in LIGHT_KEYWORDS:
        if word in text:
            return "Light"

    for word in SEWAGE_KEYWORDS:
        if word in text:
            return "Sewage"

    for word in GARBAGE_KEYWORDS:
        if word in text:
            return "Garbage"

    return "General"


def detect_priority(text: str) -> str:

    if not text:
        return "LOW"

    text = text.lower()

    CRITICAL_KEYWORDS = ["accident", "fire", "burst", "explosion",
                         "collapsed", "dead", "danger", "emergency"]

    HIGH_KEYWORDS = ["leakage", "overflow", "not working",
                     "severe", "blocked", "huge", "broken"]

    MEDIUM_KEYWORDS = ["delay", "slow", "issue", "problem",
                       "repair", "damage"]

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
