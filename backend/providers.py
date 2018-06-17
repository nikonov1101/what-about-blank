import json
import asyncio
import threading

from datetime import datetime
from urllib.parse import urlparse
from aiohttp import ClientSession
from backend import config, storage, const


class BaseJSONProvider:
    def __init__(self, url, prov_id=None, headers=None):
        self._url = urlparse(url)
        self._id = prov_id if prov_id else self._url.netloc
        self._headers = headers if headers else {'content-type': 'application/json'}

    def __str__(self) -> str:
        return self._id

    def _wrap(self, data) -> dict:
        """wraps fetched data into storage-friendly dict"""
        return dict(
            id=self._id,
            data=data,
            timestamp=datetime.now().isoformat(),
        )

    async def _fetch_json(self, url, session) -> dict:
        """asynchronously fetches data by given url, then parses JSON response into dict"""
        async with session.get(url, headers=self._headers) as response:
            data = await response.read()
            return json.loads(data)

    def process(self, data) -> dict:
        """override this method if any processing of fetched data is required"""
        return self._wrap(data)

    async def collect(self) -> dict:
        """the entrypoint of the Provider class, does all work of data-gathering"""
        async with ClientSession() as session:
            t = asyncio.ensure_future(self._fetch_json(self._url.geturl(), session))
            data = await asyncio.gather(t)
            return self.process(data)


class GithubPullRequestsProvider(BaseJSONProvider):
    def process(self, data):
        """override process method to extract only meaningful data
        from Github's PR list response.
        """

        processed = list()
        for pull in data[0]:
            processed.append(dict(
                id=pull['number'],
                author=pull['user']['login'],
                created=pull['created_at'],
                title=pull['title'],
            ))
        return self._wrap(processed)


async def collect_updates(cfg: config.Config, db: storage.Storage):
    # TODO: this should run forever
    #
    # TODO: wanna to look at previous update timestamp
    # TODO:     and decide starting related provider or not.
    tasks = [p.collect() for p in init_providers(cfg)]
    for fut in asyncio.as_completed(tasks):
        result = await fut
        pid = result['id']
        print('saving "%s" provider data' % pid)
        db.save_key(pid, result)


def init_providers(cfg: config.Config):
    return [
        GithubPullRequestsProvider(
            url=cfg.github_repo_path,
            prov_id=const.GITHUB_PULLS_PROVIDER_ID,
            headers={'accept': 'application/vnd.github.mercy-preview+json'}
        ),
    ]


def threaded_main(loop: asyncio.AbstractEventLoop, cfg: config.Config, db: storage.Storage):
    # bing given event loop to thread
    asyncio.set_event_loop(loop)
    # run async tasks bound to separate thread
    loop.run_until_complete(collect_updates(cfg, db))


def start_background_updates(cfg: config.Config, db: storage.Storage) -> threading.Thread:
    """start background processing bound to another thread,
    returns thread handle to be able to gracefully stop it
    on application shutdown."""

    # FIXME: need to find proper logging config and replace any `print`s
    print("starting background processing thread ...")
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=threaded_main, args=(loop, cfg, db))
    t.start()
    return t
