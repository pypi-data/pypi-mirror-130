#!/usr/bin/env python3
# coding: utf-8

import traceback

import orjson
from joker.environ.errors import ErrorInfo
from redis import Redis


class ErrorInterface:
    def __init__(self, redis: Redis, prefix: str, limit=1000, ttl=86400):
        self.redis = redis
        self.prefix = prefix
        self.limit = limit
        self.ttl = ttl

    def _dump(self, errinfo: ErrorInfo):
        ek = errinfo.error_key
        if self.redis.incr(f'{self.prefix}.err-count.{ek}') > 1:
            return
        debug_text = orjson.dumps(errinfo.debug_info)
        pipe = self.redis.pipeline()
        pipe.setex(f'{self.prefix}.err-debug.{ek}', self.ttl, debug_text)
        pipe.lpush(f'{self.prefix}.err-queue', ek)
        pipe.ltrim(f'{self.prefix}.err-queue', 0, self.limit)
        pipe.execute()

    def dump(self) -> ErrorInfo:
        traceback.print_exc()
        errinfo = ErrorInfo()
        self._dump(errinfo)
        return errinfo

    def query_recent_error_keys(self, n=7):
        keys = self.redis.lrange(f'{self.prefix}.err-queue', 0, n)
        return [k.decode('utf-8') for k in keys]

    def query(self, error_key: str, human=False) -> dict:
        debug_text = self.redis.get(f'{self.prefix}.err-debug.{error_key}')
        if not debug_text:
            return {}
        info = orjson.loads(debug_text)
        if human:
            exc = info.get('exc', '')
            if isinstance(exc, str):
                info['excl'] = exc.splitlines()
        return info

    def query_html(self, error_key: str, url=None):
        info = self.query(error_key)
        exc = info.get('exc')
        if not url:
            return f'<pre>{exc}<br/><a>{error_key}</a></pre>'
        return f'<pre>{exc}<br/><a href="{url}">{error_key}</a></pre>'