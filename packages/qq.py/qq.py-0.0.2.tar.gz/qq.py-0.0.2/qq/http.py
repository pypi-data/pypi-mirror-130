import asyncio
import logging
import sys
import weakref
from types import TracebackType
from typing import ClassVar, Any, Optional, Sequence, Iterable, Dict, Union, TypeVar, Type, Coroutine, List
from urllib.parse import quote as _uriquote

import aiohttp

from . import __version__, utils
from .error import HTTPException, Forbidden, NotFound, QQServerError, LoginFailure
from .gateway import QQClientWebSocketResponse
from .types import user, guild
from .utils import MISSING

T = TypeVar('T')
BE = TypeVar('BE', bound=BaseException)
MU = TypeVar('MU', bound='MaybeUnlock')
Response = Coroutine[Any, Any, T]
_log = logging.getLogger(__name__)


class Route:
    BASE: ClassVar[str] = 'https://api.sgroup.qq.com'

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.path: str = path
        self.method: str = method
        url = self.BASE + self.path
        if parameters:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        self.url: str = url

        # major parameters:
        self.channel_id: Optional[str] = parameters.get('channel_id')
        self.guild_id: Optional[str] = parameters.get('guild_id')
        self.token: Optional[str] = parameters.get('token')

    @property
    def bucket(self) -> str:
        # the bucket is just method + path w/ major parameters
        return f'{self.channel_id}:{self.guild_id}:{self.path}'


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')
    try:
        if response.headers['content-type'] == 'application/json':
            return utils._from_json(text)
    except KeyError:
        # Thanks Cloudflare
        pass

    return text


class MaybeUnlock:
    def __init__(self, lock: asyncio.Lock) -> None:
        self.lock: asyncio.Lock = lock
        self._unlock: bool = True

    def __enter__(self: MU) -> MU:
        return self

    def defer(self) -> None:
        self._unlock = False

    def __exit__(
            self,
            exc_type: Optional[Type[BE]],
            exc: Optional[BE],
            traceback: Optional[TracebackType],
    ) -> None:
        if self._unlock:
            self.lock.release()


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the Discord API."""

    def __init__(
            self,
            connector: Optional[aiohttp.BaseConnector] = None,
            *,
            proxy: Optional[str] = None,
            proxy_auth: Optional[aiohttp.BasicAuth] = None,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            unsync_clock: bool = True,
    ) -> None:
        self._locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        user_agent = 'QQ Bot (https://github.com/foxwhite25/qq.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
        self.token: Optional[str] = None
        self.proxy: Optional[str] = proxy
        self.proxy_auth: Optional[aiohttp.BasicAuth] = proxy_auth
        self._global_over: asyncio.Event = asyncio.Event()
        self._global_over.set()
        self.__session: aiohttp.ClientSession = MISSING
        self.connector = connector

    async def request(
            self,
            route: Route,
            *,
            # files: Optional[Sequence[File]] = None,
            form: Optional[Iterable[Dict[str, Any]]] = None,
            **kwargs: Any,
    ) -> Any:
        bucket = route.bucket
        method = route.method
        url = route.url

        lock = self._locks.get(bucket)
        if lock is None:
            lock = asyncio.Lock()
            if bucket is not None:
                self._locks[bucket] = lock

        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
        }

        # Add token to header
        if self.token is not None:
            headers['Authorization'] = 'Bot ' + self.token

        # Checking if it's a JSON request
        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = utils._to_json(kwargs.pop('json'))

        kwargs['headers'] = headers

        # Proxy support
        if self.proxy is not None:
            kwargs['proxy'] = self.proxy
        if self.proxy_auth is not None:
            kwargs['proxy_auth'] = self.proxy_auth

        if not self._global_over.is_set():
            # wait until the global lock is complete
            await self._global_over.wait()

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None
        await lock.acquire()
        with MaybeUnlock(lock) as maybe_lock:
            for tries in range(5):

                if form:
                    form_data = aiohttp.FormData()
                    for params in form:
                        form_data.add_field(**params)
                    kwargs['data'] = form_data
                try:
                    async with self.__session.request(method, url, **kwargs) as response:
                        _log.debug('%s %s with %s has returned %s', method, url, kwargs.get('data'), response.status)

                        # even errors have text involved in them so this is safe to call
                        data = await json_or_text(response)

                        # the request was successful so just return the text/json
                        if 300 > response.status >= 200:
                            _log.debug('%s %s has received %s', method, url, data)
                            return data

                        # we've received a 500, 502, or 504, unconditional retry
                        if response.status in {500, 502, 504}:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        # the usual error cases
                        if response.status == 403:
                            raise Forbidden(response, data)
                        elif response.status == 404:
                            raise NotFound(response, data)
                        elif response.status >= 500:
                            raise QQServerError(response, data)
                        else:
                            raise HTTPException(response, data)

                    # This is handling exceptions from the request
                except OSError as e:
                    # Connection reset by peer
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise

                if response is not None:
                    # We've run out of retries, raise.
                    if response.status >= 500:
                        raise QQServerError(response, data)

                    raise HTTPException(response, data)

                raise RuntimeError('Unreachable code in HTTP handling')

    async def static_login(self, token: str) -> user.User:
        # Necessary to get aiohttp to stop complaining about session creation
        self.__session = aiohttp.ClientSession(connector=self.connector, ws_response_class=QQClientWebSocketResponse)
        old_token = self.token
        self.token = token

        try:
            data = await self.request(Route('GET', '/users/@me'))
        except HTTPException as exc:
            self.token = old_token
            if exc.status == 401:
                raise LoginFailure('Improper token has been passed.') from exc
            raise

        return data

    def get_guilds(
        self,
        limit: int,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> Response[List[guild.Guild]]:
        params: Dict[str, Any] = {
            'limit': limit,
        }

        if before:
            params['before'] = before
        if after:
            params['after'] = after

        return self.request(Route('GET', '/users/@me/guilds'), params=params)

    def get_guild(self, guild_id: str) -> Response[guild.Guild]:
        return self.request(Route('GET', '/guilds/{guild_id}', guild_id=guild_id))
