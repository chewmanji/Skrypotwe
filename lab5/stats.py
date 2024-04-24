from datetime import datetime
from ipaddress import IPv4Address
import random
import numpy as np
from statistics import mean, pstdev
from sys import maxsize
from utils import MessageType

USERS_ENTRIES: dict[str, list[dict]] = {}
USERS_IPS: dict[str, set[IPv4Address]] = {}
USERS_SESSIONS: dict[str, dict[int, tuple[datetime, datetime]]] = {}


def update_users_dict(username: str, log_dict: dict[str, str | int | datetime]) -> None:
    """
    Updates the internal dictionary storing log entries for a specific user.

    Args:
        username (str): The username to update.
        log_dict (dict[str, str | int | datetime]): A dictionary containing a single log entry.
    """
    if username:
        if username in USERS_ENTRIES.keys():
            USERS_ENTRIES[username].append(log_dict)
        else:
            USERS_ENTRIES[username] = [log_dict]


def update_users_ips(username: str, ips: list[IPv4Address]) -> None:
    """
    Updates the internal dictionary storing unique IPv4 addresses used by a specific user.

    Args:
        username (str): The username to update.
        ips (list[IPv4Address]): A list of IPv4 addresses associated with the user's activity.
    """
    if username:
        if username not in USERS_IPS.keys():
            USERS_IPS[username] = set()

        for ip in ips:
            USERS_IPS[username].add(ip)


def random_entries_from_random_user():
    """
    Selects a random user and returns a random sample of their log entries.

    Returns:
        list[dict[str, str | int | datetime]]: A random subset of log entries from a random user.
    """
    user = random.choice(list(USERS_ENTRIES.keys()))
    number_of_entries = random.randint(1, len(USERS_ENTRIES[user]) - 1)
    return np.random.choice(USERS_ENTRIES[user], number_of_entries)


def handle_update_user_session(
    username: str, mess_type: MessageType, log_dict: dict[str, str | int | datetime]
) -> None:
    """
    Updates user session information based on the message type in a log entry.

    Args:
        username (str): The username associated with the log entry.
        mess_type (MessageType): The type of message indicated in the log entry.
        log_dict (dict[str, str | int | datetime]): A dictionary containing a single log entry.
    """
    match mess_type:
        case MessageType.SUCCESSFUL_LOG | MessageType.CONNECTION_CLOSED:
            pid = log_dict["PID"]
            timestamp = log_dict["datetime"]
            update_user_sessions(username, pid, timestamp)
        case _:
            return


def update_user_sessions(username: str, pid: int, time: datetime) -> None:
    """
    Updates the internal dictionary storing login and logout timestamps for a specific user and PID.

    Args:
        username (str): The username associated with the session.
        pid (int): The process ID for the session.
        time (datetime): The timestamp of the log entry (login or logout).
    """
    if username not in USERS_SESSIONS.keys():
        USERS_SESSIONS[username] = {}

    if pid not in USERS_SESSIONS[username].keys():
        USERS_SESSIONS[username][pid] = (time, None)
    else:
        log_in_time = USERS_SESSIONS[username][pid][0]
        if log_in_time > time:
            time = time.replace(year=time.year + 1)
        USERS_SESSIONS[username][pid] = (log_in_time, time)


def calculate_all_durations() -> list[float]:
    """
    Calculates the duration of all logged sessions across all users.

    Returns:
    list[float]: A list of session durations (in seconds) for all recorded sessions.
    """
    durations: list[float] = []
    for sessions in USERS_SESSIONS.values():
        for t1, t2 in sessions.values():
            # t2 can be none because of lack of entry about closing session
            if t2:
                durations.append((t2 - t1).total_seconds())

    return durations


def global_mean() -> float:
    """
    Calculates the average duration of all logged sessions across all users.

    Returns:
    float: The average session duration (in seconds).
    """
    return mean(calculate_all_durations())


def global_stdev() -> float:
    """
    Calculates the population standard deviation of the duration of all logged sessions across all users.

    Returns:
    float: The population standard deviation of session durations (in seconds).
    """
    return pstdev(calculate_all_durations())


def calculate_user_durations(username: str) -> list[float]:
    """
    Calculates the duration of all logged sessions for a specific user.

    Args:
    username (str): The username for which to calculate session durations.

    Returns:
    list[float]: A list of session durations (in seconds) for the specified user.
    """
    durations: list[float] = []
    for t1, t2 in USERS_SESSIONS[username].values():
        if t2:
            durations.append((t2 - t1).total_seconds())

    return durations


def user_mean(username: str) -> float:
    """
    Calculates the average duration of all logged sessions for a specific user.

    Args:
    username (str): The username for which to calculate the average session duration.

    Returns:
    float: The average session duration (in seconds) for the specified user.
    """
    return mean(calculate_user_durations(username))


def user_stdev(username: str) -> float:
    """
    Calculates the population standard deviation of the duration of all logged sessions for a specific user.

    Args:
    username (str): The username for which to calculate the session duration standard deviation.

    Returns:
    float: The population standard deviation of session durations (in seconds) for the specified user.
    """
    return pstdev(calculate_user_durations(username))


def min_max_logging_users() -> tuple[tuple[str, int], tuple[str, int]]:
    """
    Finds the user with the minimum and maximum number of logged sessions.

    Returns:
    tuple[tuple[str, int], tuple[str, int]]: A tuple containing two tuples:
    - The first tuple represents the user with the minimum number of sessions (username, count)
    - The second tuple represents the user with the maximum number of sessions (username, count)
    """
    min_user: tuple[str, int] = ("", maxsize)
    max_user: tuple[str, int] = ("", 0)
    for user, sessions in USERS_SESSIONS.items():
        number_of_logging = len(sessions)
        min_user = min(min_user, (user, number_of_logging), key=lambda x: x[1])
        max_user = max(max_user, (user, number_of_logging), key=lambda x: x[1])

    return (min_user, max_user)
