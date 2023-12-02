import re

INT_PATTERN = re.compile(r"-?\d+")


def extract_int(sentence):
    return list(map(int, INT_PATTERN.findall(sentence)))
