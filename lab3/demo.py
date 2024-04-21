from lab3.get_entries_by_code import get_entries_by_code
from lab3.get_entries_by_extension import get_entries_by_extension
from lab3.get_entries_by_ip import get_entries_by_ip
from lab3.get_failed_reads import get_failed_reads
from lab3.read_log import read_log
from lab3.sort_log import sort_log
from lab3.util import *
from lab3.log_to_dict import log_to_dict
from lab3.print_dict_entry_dates import print_dict_entry_dates

entries = read_log()
sort_log(entries, RESOURCE_SIZE)
entries_dict = log_to_dict(entries)


def entries_with_given_host_and_status_code(hostname: str, code: int = 200):
    return get_entries_by_code(get_entries_by_ip(entries, hostname), code)


def sorted_failed_entries(order_element=HOSTNAME):
    return sort_log(get_failed_reads(entries, to_merge=True), order_element)


def sorted_entries_with_given_ext(ext: str, order_element=RESOURCE_SIZE):
    return sort_log(get_entries_by_extension(entries, ext), order_element)


#print_entries(
#    entries_with_given_host_and_status_code("kip-2-sn-401.dartmouth.edu")[:10]
#)
#print_entries(sorted_failed_entries()[:10])
#print_entries(sorted_entries_with_given_ext(".jpg")[:10])


#print(entries_dict['tn.fi.aau.dk'])
#print(get_addrs(entries_dict)[:100])

print_dict_entry_dates(entries_dict)