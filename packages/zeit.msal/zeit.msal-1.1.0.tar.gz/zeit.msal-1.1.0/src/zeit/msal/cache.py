from urllib.parse import urlparse, parse_qsl
import json
import msal
import os.path

try:
    import redis
    have_redis = True
except ImportError:
    have_redis = False


class FileCache(msal.TokenCache):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def exists(self):
        return os.path.exists(self.filename)

    def load(self):
        self._cache = json.load(open(self.filename))

    def save(self):
        json.dump(self._cache, open(self.filename, 'w'))


class RedisCache(msal.TokenCache):

    def __init__(self, url, key):
        super().__init__()
        self.client = redis.from_url(url)
        self.key = key

    def exists(self):
        return self.client.get(self.key) is not None

    def load(self):
        self._cache = json.loads(self.client.get(self.key))

    def save(self):
        self.client.set(self.key, json.dumps(self._cache))


def from_url(url):
    parts = urlparse(url)
    if parts.scheme == 'file':
        return FileCache(parts.path)
    elif parts.scheme.startswith('redis'):
        if not have_redis:
            raise ValueError('Must install `redis` package')
        query = dict(parse_qsl(parts.query))
        return RedisCache(
            '%s://%s%s' % (parts.scheme, parts.netloc, parts.path),
            query['key'])
    raise ValueError('Unknown cache type %s')
