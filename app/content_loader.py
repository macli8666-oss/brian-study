import json
import os

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")

_cache = {}


def load_subject(subject_id):
    if subject_id in _cache:
        return _cache[subject_id]
    file_map = {
        "math_pure1": "math_pure1.json",
        "math_stats1": "math_stats1.json",
        "physics_as": "physics_as.json",
    }
    filename = file_map.get(subject_id)
    if not filename:
        return None
    filepath = os.path.join(CONTENT_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    _cache[subject_id] = data
    return data


def get_all_subjects():
    subjects = []
    for sid in ["math_pure1", "math_stats1", "physics_as"]:
        data = load_subject(sid)
        if data:
            subjects.append({
                "subject_id": data["subject_id"],
                "name_en": data["subject_name_en"],
                "name_zh": data["subject_name_zh"],
            })
    return subjects


def get_chapters(subject_id):
    data = load_subject(subject_id)
    if not data:
        return []
    return [
        {
            "chapter_id": ch["chapter_id"],
            "title_en": ch["title_en"],
            "title_zh": ch["title_zh"],
        }
        for ch in data["chapters"]
    ]


def get_chapter(subject_id, chapter_id):
    data = load_subject(subject_id)
    if not data:
        return None
    for ch in data["chapters"]:
        if ch["chapter_id"] == chapter_id:
            return ch
    return None


def get_knowledge_point(subject_id, chapter_id, index):
    ch = get_chapter(subject_id, chapter_id)
    if not ch or index < 0 or index >= len(ch["knowledge_points"]):
        return None, 0
    return ch["knowledge_points"][index], len(ch["knowledge_points"])


def get_question(subject_id, chapter_id, index):
    ch = get_chapter(subject_id, chapter_id)
    if not ch or index < 0 or index >= len(ch["questions"]):
        return None, 0
    return ch["questions"][index], len(ch["questions"])
