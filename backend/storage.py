import json
import logging
from threading import Lock


class Storage:
    """Storage provides simple thread-save storage singleton"""
    instance = None

    def __init__(self, path):
        if not Storage.instance:
            Storage.instance = Storage.__Storage(path)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Storage:
        mu = Lock()
        log = logging.getLogger('storage')

        def __init__(self, path):
            self.log.setLevel(logging.DEBUG)

            # try to open file and load their content as JSON
            # if it failed - file is empty, try to rewrite it with
            # an empty dict
            try:
                with open(path, 'r') as f:
                    json.loads(f.read())
                    read_ok = True
            except:
                read_ok = False
                self.log.debug('cannot read storage from %s, try to create new data-file', path, exc_info=1)

            if not read_ok:
                with open(path, 'w') as f:
                    f.write(json.dumps({}))

            self.log.debug("successfully create storage instance at %s", path)
            self._path = path

        def save_key(self, key, data):
            """saves JSON-serializable data by given key"""
            self.log.debug("save key %s", key)

            self.mu.acquire()
            try:
                current = self._load()
                current[key] = data

                serialized = json.dumps(current)
                with open(self._path, 'w') as f:
                    f.write(serialized)
            except:
                self.log.error('cannot save key "%s" into the storage', key, exc_info=1)
            finally:
                self.mu.release()

        def load_key(self, key) -> dict:
            """loads data by given key"""
            self.log.debug("load key %s", key)

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
