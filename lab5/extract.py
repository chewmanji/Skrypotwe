import re
from datetime import datetime
import ipaddress
from enum import Enum
from utils import logger, conf_logger

class MessageType(Enum):
    SUCCESSFUL_LOG = 1
    UNSUCCESSFUL_LOG = 2
    CONNECTION_CLOSED = 3
    INCORRECT_PASSWORD = 4
    INCORRECT_USERNAME = 5
    BREAK_IN_ATTEMPT = 6
    OTHER = 7


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


def get_ipv4s_from_log(
    log_dict: dict[str, str | int | datetime]
) -> list[ipaddress.IPv4Address]:
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
    pattern = r"invalid user\s+(\w+)|for user\s+(\w+)|user=(\w+)|for (root)"

    name_match: re.Match = re.search(pattern, log_dict["event"], re.I)

    if name_match is None:
        return None

    for name in name_match.groups():
        if name:
            return name


def get_message_type(event_description: str) -> MessageType | None:
    patterns = {
        MessageType.SUCCESSFUL_LOG: r"accepted password",
        MessageType.UNSUCCESSFUL_LOG: r"authentication failure",
        MessageType.CONNECTION_CLOSED: r"connection closed by|received disconnect|session closed",
        MessageType.INCORRECT_PASSWORD: r"failed password",
        MessageType.INCORRECT_USERNAME: r"invalid user",
        MessageType.BREAK_IN_ATTEMPT: r"break-in attempt",
    }

    for mess_type, pattern in patterns.items():
        if re.search(pattern, event_description, re.I):
            return mess_type

    return MessageType.OTHER