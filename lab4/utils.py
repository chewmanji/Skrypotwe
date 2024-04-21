from pathlib import Path
import os

BACKUP_FOLDER_NAME = Path(".backups")
JSON_STORY_FILE = Path("story.json")

def add_env_var():
    os.environ["BACKUPS_DIR"] = str(Path.home() / BACKUP_FOLDER_NAME)
