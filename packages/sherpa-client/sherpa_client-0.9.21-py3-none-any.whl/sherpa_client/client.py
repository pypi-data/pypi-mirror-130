import ssl
from typing import Dict, Union

import attr


@attr.s(auto_attribs=True)
class Client:
    """A class for keeping track of data related to the API"""

    base_url: str
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(5.0, kw_only=True)
    verify_ssl: Union[str, bool, ssl.SSLContext] = attr.ib(True, kw_only=True)

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in all endpoints"""
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        return attr.evolve(self, timeout=timeout)


@attr.s(auto_attribs=True)
class AuthenticatedClient(Client):
    """A Client which has been authenticated for use on secured endpoints"""

    token: str

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in authenticated endpoints"""
        return {"Authorization": f"Bearer {self.token}", **self.headers}


from .models import BearerToken, Credentials, RequestJwtTokenProjectAccessMode
from .types import UNSET, Response, Unset


@attr.s(auto_attribs=True)
class SherpaClient(AuthenticatedClient):
    """A Client logged"""

    token: str = attr.ib(init=True, default=None)

    def login(
        self,
        credentials: Credentials,
        project_filter: Union[Unset, None, str] = UNSET,
        project_access_mode: Union[Unset, None, RequestJwtTokenProjectAccessMode] = UNSET,
        annotate_only: Union[Unset, None, bool] = False,
        login_only: Union[Unset, None, bool] = False,
    ):
        """ """
        from .api.authentication import request_jwt_token

        r: Response[BearerToken] = request_jwt_token.sync_detailed(
            client=self,
            json_body=credentials,
            project_filter=project_filter,
            project_access_mode=project_access_mode,
            annotate_only=annotate_only,
            login_only=login_only,
        )
        if r.is_success:
            self.token = r.parsed.access_token
        else:
            r.raise_for_status()
