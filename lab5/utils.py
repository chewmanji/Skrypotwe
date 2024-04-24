from pathlib import Path
from datetime import datetime
import logging
import re
from enum import Enum


class MessageType(Enum):
    """
    Enumeration defining different log message types for easier classification.

    - SUCCESSFUL_LOG: Indicates a successful log message.
    - UNSUCCESSFUL_LOG: Indicates an unsuccessful log message.
    - CONNECTION_CLOSED: Indicates a connection closure event.
    - INCORRECT_PASSWORD: Indicates an incorrect password attempt.
    - INCORRECT_USERNAME: Indicates an incorrect username attempt.
    - BREAK_IN_ATTEMPT: Indicates a potential break-in attempt.
    - ERROR: Indicates an error message.
    - OTHER: Used for any message type not explicitly defined.
    """

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
    """
    Reads a log file line by line and yields each line converted to a dictionary.

    Args:
        file_path (Path): The path to the log file.

    Yields:
        dict: A dictionary containing the parsed log data for each line.

    Raises:
        FileNotFoundError: If the specified log file does not exist.
    """
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
    """
    Converts a single log line into a dictionary using a pre-compiled regular expression.

    Args:
        line (str): A single line from the log file.

    Returns:
        dict: A dictionary containing the parsed log data from the line.
    """
    match = COMPILED_REGEX.match(line)
    return convert_log_values(match.groupdict())


def convert_log_values(log_dict: dict[str, str]) -> dict[str, str | int | datetime]:
    """
    Processes a log dictionary, converting the datetime string to a `datetime` object
    and PID to an integer for improved data types.

    Args:
        log_dict (dict[str, str]): A dictionary containing log data.

    Returns:
        dict: The updated dictionary with converted data types.
    """
    log_dict["datetime"] = datetime.strptime(log_dict["datetime"], "%b %d %H:%M:%S")
    log_dict["PID"] = int(log_dict["PID"])
    return log_dict


def dict_to_string(log_dict: dict[str, str | int | datetime]) -> str:
    """
    Reconstructs a formatted log line string from a log dictionary.

    Args:
        log_dict (dict[str, str | int | datetime]): A dictionary containing log data.

    Returns:
        str: The formatted log line string.
    """
    date_str = log_dict["datetime"].strftime("%b %d %H:%M:%S")
    return f"{date_str} {log_dict['hostname']} {log_dict['component']}[{log_dict['PID']}]: {log_dict['event']}"
