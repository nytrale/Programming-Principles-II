# persistence.py — сохранение лидерборда и настроек

import json
import os

# ─────────────────────────────────────────────
# НАСТРОЙКИ
# ─────────────────────────────────────────────

DEFAULT_SETTINGS = {
    "sound": True,
    "difficulty": "normal",   # easy / normal / hard
    "car_color": "default"    # default / red / blue / green
}

SETTINGS_FILE    = "settings.json"
BASE_DIR = os.path.dirname(__file__)
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")


def load_settings():
    """Загружает настройки из файла. Если файла нет — возвращает дефолтные."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                data = json.load(f)
                # Добавляем недостающие ключи если файл старый
                for key, val in DEFAULT_SETTINGS.items():
                    if key not in data:
                        data[key] = val
                return data
        except:
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict):
    """Сохраняет настройки в файл."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# ЛИДЕРБОРД
# ─────────────────────────────────────────────

def load_leaderboard():
    """Загружает лидерборд из файла."""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []


def save_leaderboard(leaderboard: list):
    """Сохраняет лидерборд в файл."""
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)


def add_score(username: str, score: int, distance: int):
    """Добавляет результат в лидерборд и сохраняет топ 10."""
    leaderboard = load_leaderboard()
    leaderboard.append({
        "name":     username,
        "score":    score,
        "distance": distance
    })
    # Сортируем по счёту и оставляем топ 10
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(leaderboard)
    return leaderboard