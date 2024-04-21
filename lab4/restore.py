import argparse
from pathlib import Path
from utils import add_env_var, BACKUP_FOLDER_NAME, JSON_STORY_FILE
import os
import json
import subprocess
import sys


def analyze_json_file(json_file: Path) -> dict:
    with open(json_file, "r+") as file:
        archives = json.load(file)

        if archives:
            arch_dict = create_dict(archives)
            return arch_dict

        print("Nothing to restore. Quiting...")
        sys.exit(0)


def update_json_file(json_file: Path, option: int):
    with open(json_file, "r") as file:
        data: list = json.load(file)
        del data[option]

    with open(json_file, "w") as file:
        json.dump(data, file, indent=3)


def create_dict(archs_list: list):
    result = {}
    for i, arch in enumerate(archs_list):
        result[i] = arch

    return result


def print_archives(archives: dict):
    for i, arch in archives.items():
        time = arch["time"]
        source = arch["source"]
        name = arch["name"]
        print(f"Option ({i+1}):\n\tTIME = {time}\n\tSOURCE = {source}\n\tNAME = {name}")


def get_user_option(arch_dict: dict):
    try:
        option = int(input("Give a number of file to restore: ")) - 1
    except ValueError:
        print("Give correct number or Ctrl+C to leave")
        return get_user_option()

    if option not in arch_dict.keys():
        print("Wrong number!")
        return get_user_option(arch_dict)

    return option


def extract_archive(archive: Path, extract_path: Path):
    subprocess.run(["tar", "-xvf", archive, "-C", extract_path])


def get_archive_path(archive_dict: dict, backups: Path):
    return backups / Path(archive_dict["name"])


def delete_archive_file(path: Path):
    os.remove(path)


def main(target_path: Path):
    if "BACKUPS_DIR" not in os.environ.keys():
        add_env_var()

    backups_path = Path(os.environ["BACKUPS_DIR"])
    json_file = backups_path / JSON_STORY_FILE

    if not json_file.exists():
        print(f"Nothing to restore from {target_path}. Quiting...")
        return

    archs = analyze_json_file(json_file)

    print_archives(archs)

    user_option = get_user_option(archs)
    archive_path = get_archive_path(archs[user_option], backups_path)

    extract_archive(archive_path, target_path)
    delete_archive_file(archive_path)
    
    update_json_file(json_file, user_option)

    print("Succesfully extracted and deleted archive")
    print(f"Archive [{archive_path}] extracted to [{target_path}]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="restore chosen archive from a given folder"
    )
    parser.add_argument("--target_path", "-p")
    args = parser.parse_args()

    if not args.target_path:
        target_path = Path(os.getcwd() / BACKUP_FOLDER_NAME)
    else:
        target_path = Path(args.target_path).resolve()

    if not target_path.exists():
        os.mkdir(target_path)

    main(target_path)

    # if target_path.exists():
    #     main(target_path.absolute())
    # else:
    #     print("Given folder doesn't exist or you don't have access to it!")
