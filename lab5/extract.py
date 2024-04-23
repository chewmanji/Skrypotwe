import re
from datetime import datetime
import ipaddress
from utils import *


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
    # pattern = r"invalid user\s+(\w+)|for user\s+(\w+)|user=(\w+)|for (root|\w+)"
    pattern = r"invalid user\s+(\w+)|for user\s+(\w+)|\buser=(\w+)|(?<=for )(\w+)"

    name_match: re.Match = re.search(pattern, log_dict["event"], re.I)

    if name_match is None:
        return None

    for name in name_match.groups():
        if name:
            return name


def get_message_type(log_dict: dict[str, str | int | datetime]) -> MessageType | None:
    event_description = log_dict["event"]

    patterns = {
        MessageType.SUCCESSFUL_LOG: r"accepted password",
        MessageType.UNSUCCESSFUL_LOG: r"authentication failure",
#        MessageType.CONNECTION_CLOSED: r"connection closed by|received disconnect|session closed",
        MessageType.CONNECTION_CLOSED: r"session closed",
        MessageType.INCORRECT_PASSWORD: r"failed password",
        MessageType.INCORRECT_USERNAME: r"invalid user",
        MessageType.BREAK_IN_ATTEMPT: r"break-in attempt",
    }

    for mess_type, pattern in patterns.items():
        if re.search(pattern, event_description, re.I):
            message_type_logging_handler(mess_type, log_dict, event_description)
            return mess_type

    return MessageType.OTHER


def message_type_logging_handler(
    message_type: MessageType, log_dict: dict, event_description: str
) -> None:
    
    username = get_user_from_log(log_dict)

    match message_type:
        case MessageType.SUCCESSFUL_LOG:
            logger_out.info(
                f"""{username} has successfully logged in.
                Event descritpion: {event_description}"""
            )
        case MessageType.CONNECTION_CLOSED:
            logger_out.info(
                f"""{username} has successfully closed a session.
                Event descritpion: {event_description}"""
            )
        case MessageType.UNSUCCESSFUL_LOG | MessageType.INCORRECT_PASSWORD | MessageType.INCORRECT_USERNAME:
            logger_out.warning(
                f"""{username} tried to log in but failed.
                Event description: {event_description}"""
            )
        case MessageType.BREAK_IN_ATTEMPT:
            logger_err.critical(
                f"""{username} probably tried to break-in!!!
                Event description: {event_description}"""
            )
        case _:
            pass
