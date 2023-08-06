import yaml
from .internals import pull, push, get_storage_path, put


class Storage:
    def __init__(self, name):
        self.name = name

    def __call__(self, key):
        return Entry(self.name, key)


class Entry:
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def _act(self, function, value):
        path = get_storage_path(self.name)

        if path.exists():
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
        else:
            data = {}

        was_modified, result = function(data, self.key.split('.'), value)

        if was_modified:
            with open(path, 'w') as f:
                yaml.safe_dump(data, f)

        return was_modified, result

    def pull(self, value=None):
        return self._act(pull, value)[1]

    def push(self, value=True):
        return self._act(push, value)[1]

    def put(self, value=True):
        return self._act(put, value)[1]

    def try_push(self, value=True):
        return self._act(push, value)[0]

    def try_put(self, value=True):
        return self._act(put, value)[0]
