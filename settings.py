import json

# Default settings
default_settings = {
    "sound": True,
    "weapon_sounds": {
        "Start": "sounds/startShot.mp3",
        "Relic": "sounds/relicShot.mp3"
    }
}

# Load settings
def load_settings():
    try:
        with open("settings.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default settings if the file is missing or corrupted
        save_settings(default_settings)
        return default_settings

# Save settings
def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)

settings = load_settings()  # Load settings at the start

