import datetime
import json
import random
import string
from typing import Callable, Sequence


def generate_random_filename():
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    return f"{ts}_{file_name}"

def distinct_by(s: Sequence, key_selector: Callable):
    keys = set()
    for i in s:
        key = key_selector(i)
        if key not in keys:
            keys.add(key)
            yield i

class JsonSerilaizable:
    def to_serializable(self):
        raise NotImplementedError('users must define "to_serializable" to use this base class')


class JsonSerializableEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, JsonSerilaizable):
            return obj.to_serializable()
        else:
            return super(JsonSerializableEncoder, self).default(obj)

