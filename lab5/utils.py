from pathlib import Path
from datetime import datetime
from extract import COMPILED_REGEX
import logging
import sys

logger = logging.getLogger(__name__)

def read_log_file(file_path: Path):
    conf_logger(logger, logging.DEBUG, sys.stdout)
    try:
        with open(file_path, "r") as file:
            for line in file:
                logger.debug(f"Read bytes: {len(line.encode())}")
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


def conf_logger(logger : logging.Logger, severity, output):
    logger.setLevel(severity)
    handler = logging.StreamHandler(output)
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
