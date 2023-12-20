import bisect
import re

INT_PATTERN = re.compile(r"-?\d+")


def extract_int(sentence):
    return list(map(int, INT_PATTERN.findall(sentence)))


def insert_sorted(seq, keys, item, key_func=lambda v: v):
    k = key_func(item)
    i = bisect.bisect_left(keys, k)
    keys.insert(i, k)
    seq.insert(i, item)
