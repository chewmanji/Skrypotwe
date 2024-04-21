from os import environ, X_OK, listdir, access
from pathlib import Path
import argparse


paths_list = environ["PATH"].split(";")


def walktree(current_root: Path, print_execs: bool, visited: set):
    try:
        if current_root.exists() and current_root not in visited:
            visited.add(current_root)
            for path in current_root.iterdir():
                if path.is_dir():
                    print(path)

                    if print_execs:
                        for file in listdir(path):
                            if is_executable(append_paths(path, file)):
                                print(f"\t{file}")

                    walktree(path, print_execs, visited)

    except PermissionError:
        print(f"Skipping {current_root} due to permission restrictions.")


def is_executable(path: Path) -> bool:
    if path.is_file():
        return access(path, X_OK)
    return False


def append_paths(parent: Path, file: str):
    return parent / file


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Wypisuje wszystkie katalogi z folderów w zmiennej PATH"
    )
    parser.add_argument(
        "--execs",
        "-x",
        action="store_true",
        help="wypisz pliki wykonywalne w folderach",
    )
    args = parser.parse_args()
    visited = set()
    for path in paths_list:
        walktree(Path(path), args.execs, visited)
