"""Define a client to interact with Flu Near You."""
import logging
from typing import Any, Dict, Optional, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .cdc import CdcReport
from .errors import RequestError
from .user import UserReport

_LOGGER: logging.Logger = logging.getLogger(__name__)

DEFAULT_CACHE_SECONDS = 60 * 60
DEFAULT_HOST = "api.v2.flunearyou.org"
DEFAULT_ORIGIN = "https://flunearyou.org"
DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = "Home Assistant (Macintosh; OS X/10.14.0) GCDHTTPRequest"

API_URL_SCAFFOLD = f"https://{DEFAULT_HOST}"


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
        self,
        *,
        cache_seconds: int = DEFAULT_CACHE_SECONDS,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize."""
        self._cache_seconds = cache_seconds
        self._session: Optional[ClientSession] = session
        self.cdc_reports = CdcReport(self._request, cache_seconds)
        self.user_reports = UserReport(self._request, cache_seconds)

    async def _request(
        self, method: str, endpoint: str, **kwargs: Dict[str, Any]
    ) -> dict:
        """Make a request against Flu Near You."""
        kwargs.setdefault("headers", {})
        kwargs["headers"].update(
            {
                "Host": DEFAULT_HOST,
                "Origin": DEFAULT_ORIGIN,
                "Referrer": DEFAULT_ORIGIN,
                "User-Agent": DEFAULT_USER_AGENT,
            }
        )

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        assert session

        try:
            async with session.request(
                method, f"{API_URL_SCAFFOLD}/{endpoint}", **kwargs
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
        except ClientError as err:
            raise RequestError(
                f"Error requesting data from {endpoint}: {err}"
            ) from None
        finally:
            if not use_running_session:
                await session.close()

        return cast(Dict[str, Any], data)
