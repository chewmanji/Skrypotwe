from typing import Match
from lab2.util import extract_log


def extract_resource_size(log: Match) -> int:
    if log:
        bytes = log.group("bytes")
        return int(bytes if bytes else 0) #bytes are optional group in regex that's why there's check if it's not None
    return 0


if __name__ == "__main__":
    result = 0
    while True:
        try:
            log = input()
            match = extract_log(log)
            result += extract_resource_size(match)
        except EOFError:
            print(f"Data send to hosts: {result/(1024**3)} GB")
            break
