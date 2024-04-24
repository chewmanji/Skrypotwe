from pathlib import Path
import argparse
from extract import *
from utils import read_log_file, MessageType, dict_to_string
import logging
from logging_conf import *
from stats import *


def log_entry(message_type: MessageType, user: str, event_description: str):
    message_type_logging_handler(message_type, user, event_description)


def extract_handler(
    args,
    ips: list,
    user: str,
    mess_type: MessageType,
    log_dict: dict[str, str | int | datetime],
):
    info: str = f"ENTRY: {dict_to_string(log_dict)}"
    if args.ips:
        info += f"\n\tIPS: {ips}"
    if args.user:
        info += f"\n\tUSER: {user}"
    if args.message:
        info += f"\n\tMessage: {mess_type}"

    if args.ips or args.user or args.type:
        print(info)


def stats_handler(args):
    if args.random:
        entries = random_entries_from_random_user()
        print(f"Here are random number of entries releated to random user:")
        for entry in entries:
            print(f"\t{dict_to_string(entry)}")
    if args.all:
        print(f"Global MEAN = {global_mean()} sec")
        print(f"Global STDEV = {global_stdev()} sec")
    if args.min_max:
        result = min_max_logging_users()
        print(f"USER: {result[0][0]} | Logging in number: {result[0][1]}")
        print(f"USER: {result[1][0]} | Logging in number: {result[1][1]}")
    if args.user:
        if args.user in USERS_SESSIONS.keys():
            print(
                f"Mean value for [{args.user}]: {user_mean(args.user)} sec\nStandard deviation for [{args.user}]: {user_stdev(args.user)} sec"
            )
        else:
            print(f"No such user was found in log file. USER = {args.user}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", required=True, help="Path to log file")
    parser.add_argument(
        "--log",
        "-l",
        required=False,
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Level of logging",
    )
    parser.add_argument(
        "--nolog", action="store_false", required=False, help="Don't log information"
    )

    subparsers = parser.add_subparsers(help="sub-command help", dest="subcommand")

    parser_extract = subparsers.add_parser(
        "extract", help="extract information from log entry"
    )
    parser_extract.add_argument(
        "--ips", "-i", action="store_true", help="Return ipv4s from log entry"
    )
    parser_extract.add_argument(
        "--user", "-u", action="store_true", help="Return user from log entry"
    )
    parser_extract.add_argument(
        "--message",
        "-m",
        action="store_true",
        help="Return message type from log entry",
    )
    parser_extract.set_defaults(func=extract_handler)

    parser_stats = subparsers.add_parser("stats", help="stats sub-command")
    parser_stats.add_argument(
        "--random",
        "-r",
        action="store_true",
        help="Return random entries from random user",
    )
    parser_stats.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Calculate global mean and standard deviation of connection durations",
    )
    parser_stats.add_argument(
        "--user",
        "-u",
        help="Calculate user mean  and standard deviation of connection durations",
    )
    parser_stats.add_argument(
        "--min_max", "-mm", action="store_true", help="Return min/max logging in users"
    )
    parser_stats.set_defaults(func=stats_handler)

    args = parser.parse_args()

    if args.nolog:
        loglevel = args.log
        numeric_level = getattr(logging, loglevel, None)
        conf_root_logger(numeric_level)

    # main loop
    for entry in read_log_file(Path(args.path)):
        mess_type = get_message_type(entry)
        user = get_user_from_log(entry)
        ips = get_ipv4s_from_log(entry)

        if args.nolog:
            log_entry(mess_type, user, entry["event"])

        if args.subcommand == "extract":
            args.func(args, ips, user, mess_type, entry)

        update_users_dict(user, entry)
        update_users_ips(user, ips)
        handle_update_user_session(user, mess_type, entry)

    args.func(args)
