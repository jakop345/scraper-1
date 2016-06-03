from datetime import timedelta
from functools import partial
from collections import OrderedDict
import re

from slugify import slugify as _slugify

slugify = partial(_slugify, to_lower=True, max_length=50)

DURATION_RE = re.compile(
    '^(?P<neg>-?)'
    'P((?P<years>\d+)Y)?'
    '((?P<months>\d+)M)?'
    '((?P<days>\d+)D)?'
    '(?P<Time>T'
    '((?P<hours>\d+)H)?'
    '((?P<minutes>\d+)M)?'
    '(((?P<seconds>\d+)'
    '(?P<fracsec>\.\d+)?)S)?)?$')


def duration_as_seconds(duration):
    d = DURATION_RE.match(duration).groupdict(0)
    delta = timedelta(
        days=int(d['days']) + (int(d['months']) * 30) + (int(d['years']) * 365),
        hours=int(d['hours']), minutes=int(d['minutes']), seconds=int(d['seconds']))

    if d['neg'] == "-":
        delta *= -1

    return int(delta.total_seconds())


def order_dict(dictionary, sort_using):
    result = OrderedDict()

    for key in sort_using:
        result[key] = dictionary[key]

    return result
