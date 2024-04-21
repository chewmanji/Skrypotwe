import argparse
from utils import add_env_var, JSON_STORY_FILE
from pathlib import Path
import subprocess
import datetime
import os
import shutil
import json


def update_json_file(time, folder_path, archive_name, backups_path):
    path_json = backups_path / JSON_STORY_FILE
    if not path_json.exists():
        path_json.touch()

    row = {
        "time": datetime.datetime.strptime(time, "%Y%m%d%H%M%S").strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "source": str(folder_path),
        "name": archive_name,
    }

    with open(path_json, "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []  # Empty list for new data

        data.append(row)
        file.seek(0)
        json.dump(data, file, indent=3)


def move_archive(archive_path: Path, backups_path: Path):
    if not backups_path.exists():
        os.mkdir(backups_path)

    print(archive_path, backups_path)
    # subprocess.run(["move", archive_path, backups_path]) ---> tu nie dziala move windowsowy
    shutil.move(archive_path, backups_path)


def create_archive(path: Path):
    archive_name = f"{create_timestamp_str()}-{path.name}.tar"
    print(archive_name)
    subprocess.run(["tar", "-cvf", archive_name, path])
    return Path.cwd() / Path(archive_name)


def create_timestamp_str(time: datetime.datetime = datetime.datetime.now()) -> str:
    return time.strftime("%Y%m%d%H%M%S")


def main(path: Path):
    arch_path: Path = create_archive(path)

    if "BACKUPS_DIR" not in os.environ.keys():
        add_env_var()

    backups_path = Path(os.environ["BACKUPS_DIR"])

    move_archive(arch_path, backups_path)

    update_json_file(
        arch_path.name.partition("-")[0], path, arch_path.name, backups_path
    )  # str.partition zwraca 3-elementowa tuple z separatorem i dwiema czesciami


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="create backup for a given folder")
    parser.add_argument("--path", "-p")
    args = parser.parse_args()
    path = Path(args.path)
    if path.exists():
        main(path.resolve())
    else:
        print("Given folder doesn't exist or you don't have access to it!")
