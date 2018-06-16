import json
from threading import Lock


class Storage:
    """Storage provides simple thread-save storage"""
    mu = Lock()

    def __init__(self, path):
        # try to open file and load their content as JSON
        # if it failed - file is empty, try to rewrite it with
        # an empty dict
        try:
            with open(path, 'r') as f:
                json.loads(f.read())
                read_ok = True
        except:
            read_ok = False

        if not read_ok:
            with open(path, 'w') as f:
                f.write(json.dumps({}))

        self._path = path

    def save_key(self, key, data):
        """saves JSON-serializable data by given key"""
        self.mu.acquire()
        try:
            current = self._load()
            current[key] = data

            serialized = json.dumps(current)
            with open(self._path, 'w') as f:
                f.write(serialized)

        finally:
            self.mu.release()

    def load_key(self, key) -> dict:
        """loads data by given key"""
        data = self.load_all()
        try:
            v = data[key]
        except KeyError:
            v = None

        return v

    def load_all(self) -> dict:
        """loads all data from storage"""
        self.mu.acquire()
        try:
            data = self._load()
        finally:
            self.mu.release()

        return data

    def _load(self):
        """reads data from state file, need to be protected by mutex"""
        with open(self._path, 'r') as f:
            return json.loads(f.read())
