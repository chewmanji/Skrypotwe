from typing import Match
from lab2.util import extract_log
from lab2.reduction_functions.task_3_b import extract_resource_size
import re

pattern = re.compile(r"^(\S+|\s+)")


def extract_path_to_resource(log: Match) -> str:
    if log:
        path = re.search(
            pattern, log.group("path")
        )  # extract path from 'path' subgroup where is also a http method
        return path.group(1)
    return ''


if __name__ == "__main__":
    path_to_biggest = ""
    size_biggest = 0
    while True:
        try:
            log = input()
            match = extract_log(log)
            size = extract_resource_size(match)
            if size > size_biggest:
                size_biggest = size
                path_to_biggest = extract_path_to_resource(match)

        except EOFError:
            print(
                f"The biggest resource is: {path_to_biggest} and its size is {size_biggest} bytes"
            )
            break
