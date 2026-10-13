"""Thin requests wrapper: single place for base URL, timeouts and logging."""
import logging

import requests

from utils.config import Config

log = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = (base_url or Config.API_BASE_URL).rstrip("/")
        self.timeout = timeout or Config.API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        log.info("%s %s", method.upper(), url)
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        log.info("-> %s in %.0f ms", response.status_code,
                 response.elapsed.total_seconds() * 1000)
        return response

    def get(self, path, **kw):
        return self._request("GET", path, **kw)

    def post(self, path, **kw):
        return self._request("POST", path, **kw)

    def put(self, path, **kw):
        return self._request("PUT", path, **kw)

    def patch(self, path, **kw):
        return self._request("PATCH", path, **kw)

    def delete(self, path, **kw):
        return self._request("DELETE", path, **kw)

    def close(self):
        self.session.close()
