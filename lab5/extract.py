import re
from datetime import datetime
import ipaddress
from utils import *


def get_ipv4s_from_log(
    log_dict: dict[str, str | int | datetime]
) -> list[ipaddress.IPv4Address]:
    """
    Extracts valid IPv4 addresses from the "event" field of a log dictionary.

    Args:
        log_dict (dict[str, str | int | datetime]): A dictionary containing parsed log data.

    Returns:
        list[ipaddress.IPv4Address]: A list of valid IPv4 addresses found in the event message.
    """
    ips: list[str] = re.findall(COMPILED_IPV4_PATTERN, log_dict["event"])

    valid_ips = []

    # performance issues???
    for ip in ips:
        try:
            valid_ips.append(
                ipaddress.ip_address(ip)
            )  # no list comprehension because of 1 line which raises exception...
        except ValueError:
            pass

    return valid_ips


def get_user_from_log(log_dict: dict[str, str | int | datetime]) -> str | None:
    """
    Attempts to extract the username from the "event" field of a log dictionary using a regular expression.

    Args:
        log_dict (dict[str, str | int | datetime]): A dictionary containing parsed log data.

    Returns:
        str | None: The extracted username if found, otherwise None.
    """
    pattern = r"invalid user\s+(\w+)|for user\s+(\w+)|\buser=(\w+)|(?<=for )([a-zA-Z]+)"

    name_match: re.Match = re.search(pattern, log_dict["event"], re.I)

    if name_match is None:
        return None

    for name in name_match.groups():
        if name:
            return name


def get_message_type(log_dict: dict[str, str | int | datetime]) -> MessageType:
    """
    Classifies the log message type based on patterns in the "event" field of a log dictionary.

    Args:
        log_dict (dict[str, str | int | datetime]): A dictionary containing parsed log data.

    Returns:
        MessageType: The identified message type.
    """
    event_description = log_dict["event"]

    patterns = {
        MessageType.SUCCESSFUL_LOG: r"accepted password",
        MessageType.UNSUCCESSFUL_LOG: r"authentication failure",
        MessageType.CONNECTION_CLOSED: r"session closed",
        MessageType.INCORRECT_PASSWORD: r"failed password",
        MessageType.INCORRECT_USERNAME: r"invalid user",
        MessageType.BREAK_IN_ATTEMPT: r"break-in attempt",
        MessageType.ERROR: r"error: ",
    }

    for mess_type, pattern in patterns.items():
        if re.search(pattern, event_description, re.I):
            return mess_type

    return MessageType.OTHER
