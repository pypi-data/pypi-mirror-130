from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.flawdb_api_v1_flaws_destroy_format import FlawdbApiV1FlawsDestroyFormat
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, FlawdbApiV1FlawsDestroyFormat] = UNSET,
) -> Dict[str, Any]:
    url = "/flawdb/api/v1/flaws/{id}".format(
        id=id,
    )

    json_format_: Union[Unset, None, str] = UNSET
    if not isinstance(format_, Unset):

        json_format_ = FlawdbApiV1FlawsDestroyFormat(format_).value if format_ else None

    params: Dict[str, Any] = {
        "format": json_format_,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, FlawdbApiV1FlawsDestroyFormat] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        id=id,
        client=client,
        format_=format_,
    )

    response = client.get_session().delete(
        **kwargs,
    )
    response.raise_for_status()

    return _build_response(response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, FlawdbApiV1FlawsDestroyFormat] = UNSET,
) -> Response[Any]:
    kwargs = _get_kwargs(
        id=id,
        client=client,
        format_=format_,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
