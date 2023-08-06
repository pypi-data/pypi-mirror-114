from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.user import User
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    username: str,
) -> Dict[str, Any]:
    url = "{}/users/{username}".format(client.base_url, username=username)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, User]]:
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 500:
        response_500 = None

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, User]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    username: str,
) -> Response[Union[Any, User]]:
    kwargs = _get_kwargs(
        client=client,
        username=username,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    username: str,
) -> Optional[Union[Any, User]]:
    """Returns the user with the given username if it exists. For security reasons the hashed password is omitted in the response"""

    return sync_detailed(
        client=client,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    username: str,
) -> Response[Union[Any, User]]:
    kwargs = _get_kwargs(
        client=client,
        username=username,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    username: str,
) -> Optional[Union[Any, User]]:
    """Returns the user with the given username if it exists. For security reasons the hashed password is omitted in the response"""

    return (
        await asyncio_detailed(
            client=client,
            username=username,
        )
    ).parsed
