import json
import asyncio

from datetime import datetime
from urllib.parse import urlparse
from aiohttp import ClientSession


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


async def main(providers):
    tasks = [p.collect() for p in providers]
    for fut in asyncio.as_completed(tasks):
        result = await fut
        print('returns {}'.format(result))


def get_providers():
    return [
        GithubPullRequestsProvider(
            prov_id='github_core_pulls',
            url='https://api.github.com/repos/sonm-io/core/pulls',
            headers={'accept': 'application/vnd.github.mercy-preview+json'}
        ),
    ]


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(get_providers()))
