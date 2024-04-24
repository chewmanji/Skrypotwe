from pathlib import Path
from datetime import datetime
import logging
import re
from enum import Enum


class MessageType(Enum):
    SUCCESSFUL_LOG = 1
    UNSUCCESSFUL_LOG = 2
    CONNECTION_CLOSED = 3
    INCORRECT_PASSWORD = 4
    INCORRECT_USERNAME = 5
    BREAK_IN_ATTEMPT = 6
    ERROR = 7
    OTHER = 8


PATTERN = r"""
(?P<datetime>\w+\s+\d+\s+\d+:\d+:\d+)\s+
(?P<hostname>\w+)\s+
(?P<component>\w+)
\[(?P<PID>\d+)\]:\s+
(?P<event>.*)
"""
COMPILED_REGEX = re.compile(PATTERN, re.X)

IPV4_PATTERN = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

COMPILED_IPV4_PATTERN = re.compile(IPV4_PATTERN)


def read_log_file(file_path: Path):
    try:
        with open(file_path, "r") as file:
            for line in file:
                logging.debug(
                    f"Read bytes: {len(line)}"
                )  # isn't it in the wrong place?
                yield line_to_dict(line)

    except FileNotFoundError:
        print(f"File [{file_path.resolve()}] doesn't exist.")


def line_to_dict(line: str) -> dict[str, str | int | datetime]:
    match = COMPILED_REGEX.match(line)
    return convert_log_values(match.groupdict())


def convert_log_values(log_dict: dict[str, str]) -> dict[str, str | int | datetime]:
    log_dict["datetime"] = datetime.strptime(log_dict["datetime"], "%b %d %H:%M:%S")
    log_dict["PID"] = int(log_dict["PID"])
    return log_dict

def dict_to_string(log_dict: dict[str, str | int | datetime]) -> str:
    date_str = log_dict["datetime"].strftime("%b %d %H:%M:%S")
    return f"{date_str} {log_dict['hostname']} {log_dict['component']}[{log_dict['PID']}]: {log_dict['event']}"