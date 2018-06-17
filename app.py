from backend import const, providers, storage, config
from flask import Flask, jsonify


class Server(Flask):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        # looks like the crutch of the year.
        self.cfg = config.Config('config.yaml')
        self.storage = storage.Storage(self.cfg.storage_path)


app = Server(__name__)


@app.route('/github')
def github():
    data = app.storage.load_key(const.GITHUB_PULLS_PROVIDER_ID)
    return jsonify({'data': data})


if __name__ == '__main__':
    background_thread = providers.start_background_updates(app.cfg, app.storage)

    try:
        # todo: fill server params from config
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print('stopping app ...')
        background_thread._tstate_lock.release()
        background_thread._stop()
