import yaml


class Config:
    _data = dict()

    def __init__(self, path):
        with open(path, 'r') as f:
            data = yaml.load(f.read())

        errors = self._validate(data)
        if errors:
            raise ValueError('Config file contains errors: {}'.format('; '.join(errors)))

        self._data = data

    def _validate(self, data) -> list:
        # todo: this is droch, find some fancy lib for config parsing
        # or at least use cerberus as schema validator
        errors = list()
        try:
            if not data['backend']['storage']:
                errors.append('"storage" parameter is required')
            if not data['backend']['endpoint']:
                errors.append('"endpoint" parameter is required')
        except KeyError:
            errors.append('"backend" section is required')

        try:
            if not data['providers']['github_pulls']:
                errors.append('"github_pulls" parameter is required')
        except KeyError:
            errors.append('"providers" section is required')

        return errors

    @property
    def storage_path(self):
        return self._data['backend']['storage']

    @property
    def backend_endpoint(self):
        return self._data['backend']['endpoint']

    @property
    def github_repo_path(self):
        repo = self._data['providers']['github_pulls']
        return 'https://api.github.com/repos/{}/pulls'.format(repo)
