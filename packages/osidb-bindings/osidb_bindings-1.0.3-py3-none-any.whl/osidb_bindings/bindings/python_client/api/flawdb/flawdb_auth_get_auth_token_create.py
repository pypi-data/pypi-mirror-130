from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.auth_token import AuthToken
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    form_data: AuthToken,
    multipart_data: AuthToken,
    json_body: AuthToken,
) -> Dict[str, Any]:
    url = "/flawdb/auth/get_auth_token/"

    json_json_body: Dict[str, Any] = UNSET
    if not isinstance(json_body, Unset):
        json_body.to_dict()

    multipart_multipart_data: Dict[str, Any] = UNSET
    if not isinstance(multipart_data, Unset):
        multipart_data.to_multipart()

    return {
        "url": url,
        "data": form_data.to_dict(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[AuthToken]:
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: AuthToken
        if isinstance(_response_200, Unset):
            response_200 = UNSET
        else:
            response_200 = AuthToken.from_dict(_response_200)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AuthToken]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    form_data: AuthToken,
    multipart_data: AuthToken,
    json_body: AuthToken,
) -> Response[AuthToken]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    )

    response = client.get_session().post(
        **kwargs,
    )
    response.raise_for_status()

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    form_data: AuthToken,
    multipart_data: AuthToken,
    json_body: AuthToken,
) -> Optional[AuthToken]:
    """ """

    return sync_detailed(
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    form_data: AuthToken,
    multipart_data: AuthToken,
    json_body: AuthToken,
) -> Response[AuthToken]:
    kwargs = _get_kwargs(
        client=client,
        form_data=form_data,
        multipart_data=multipart_data,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    form_data: AuthToken,
    multipart_data: AuthToken,
    json_body: AuthToken,
) -> Optional[AuthToken]:
    """ """

    return (
        await asyncio_detailed(
            client=client,
            form_data=form_data,
            multipart_data=multipart_data,
            json_body=json_body,
        )
    ).parsed
