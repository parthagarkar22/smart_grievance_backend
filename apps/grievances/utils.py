def detect_department(text: str) -> str:
    """
    Auto-detect department based on grievance description/title
    """

    if not text:
        return "General"

    text = text.lower()

    WATER_KEYWORDS = [
        "water", "pipe", "leak", "leakage", "tap", "supply"
    ]

    ROAD_KEYWORDS = [
        "road", "pothole", "street", "bridge", "footpath"
    ]

    LIGHT_KEYWORDS = [
        "light", "electric", "electricity", "lamp", "street light", "power"
    ]

    SEWAGE_KEYWORDS = [
        "sewage", "drain", "gutter", "manhole", "overflow"
    ]

    GARBAGE_KEYWORDS = [
        "garbage", "waste", "trash", "dump", "dirty", "cleaning"
    ]

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
    """
    Auto-detect priority from grievance text
    """

    if not text:
        return "LOW"

    text = text.lower()

    CRITICAL_KEYWORDS = [
        "accident", "fire", "burst", "explosion",
        "collapsed", "dead", "danger", "emergency"
    ]

    HIGH_KEYWORDS = [
        "leakage", "overflow", "not working",
        "severe", "blocked", "huge", "broken"
    ]

    MEDIUM_KEYWORDS = [
        "delay", "slow", "issue", "problem",
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




# from difflib import SequenceMatcher
# import hashlib


# def calculate_text_similarity(text1, text2):
#     return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


# def get_image_hash(image_file):
#     image_file.seek(0)
#     return hashlib.md5(image_file.read()).hexdigest()


# Heavy AI deps are loaded lazily so migrate/collectstatic work on Render
# without torch/clip/sentence-transformers installed at build time.

_text_model = None
_clip_model = None
_clip_preprocess = None
_device = "cpu"


def _get_text_model():
    global _text_model
    if _text_model is None:
        from sentence_transformers import SentenceTransformer
        _text_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _text_model


def _get_clip():
    global _clip_model, _clip_preprocess
    if _clip_model is None:
        import clip
        _clip_model, _clip_preprocess = clip.load("ViT-B/32", device=_device)
    return _clip_model, _clip_preprocess


# ======================================================
# 🧠 DEPARTMENT DETECTION
# ======================================================

def detect_department(text: str) -> str:
    """
    Auto-detect department based on grievance description/title
    """

    if not text:
        return "General"

    text = text.lower()

    WATER_KEYWORDS = [
        "water", "pipe", "leak", "leakage", "tap", "supply"
    ]

    ROAD_KEYWORDS = [
        "road", "pothole", "street", "bridge", "footpath"
    ]

    LIGHT_KEYWORDS = [
        "light", "electric", "electricity", "lamp", "street light", "power"
    ]

    SEWAGE_KEYWORDS = [
        "sewage", "drain", "gutter", "manhole", "overflow"
    ]

    GARBAGE_KEYWORDS = [
        "garbage", "waste", "trash", "dump", "dirty", "cleaning"
    ]

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


# ======================================================
# ⚡ PRIORITY DETECTION
# ======================================================

def detect_priority(text: str) -> str:
    """
    Auto-detect priority from grievance text
    """

    if not text:
        return "LOW"

    text = text.lower()

    CRITICAL_KEYWORDS = [
        "accident", "fire", "burst", "explosion",
        "collapsed", "dead", "danger", "emergency"
    ]

    HIGH_KEYWORDS = [
        "leakage", "overflow", "not working",
        "severe", "blocked", "huge", "broken"
    ]

    MEDIUM_KEYWORDS = [
        "delay", "slow", "issue", "problem",
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


# ======================================================
# 🧠 TEXT EMBEDDING
# ======================================================

def get_text_embedding(text):
    """
    Convert text into vector embedding
    """
    return _get_text_model().encode(text).tolist()


# ======================================================
# 🖼️ IMAGE EMBEDDING
# ======================================================

def get_image_embedding(image_path):
    """
    Convert image into vector embedding
    """
    import torch
    from PIL import Image

    clip_model, preprocess = _get_clip()
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(_device)

    with torch.no_grad():
        embedding = clip_model.encode_image(image)

    return embedding[0].tolist()


# ======================================================
# 📊 COSINE SIMILARITY
# ======================================================

def cosine_sim(vec1, vec2):
    """
    Calculate similarity between two vectors
    """
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity([vec1], [vec2])[0][0]


# ======================================================
# 📍 DISTANCE CALCULATION
# ======================================================

def get_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geo points (in KM)
    """
    from geopy.distance import geodesic
    return geodesic((lat1, lon1), (lat2, lon2)).km