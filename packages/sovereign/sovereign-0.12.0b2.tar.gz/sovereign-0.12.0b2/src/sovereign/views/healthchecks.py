from typing import List
from fastapi import Response, Request
from fastapi.routing import APIRouter
from fastapi.responses import PlainTextResponse
from sovereign import __version__, json_response_class
from sovereign import discovery
from sovereign.utils.mock import mock_discovery_request


router = APIRouter()


@router.get("/healthcheck", summary="Healthcheck (Does the server respond to HTTP?)")
async def health_check() -> Response:
    return PlainTextResponse("OK")


@router.get(
    "/deepcheck",
    summary="Deepcheck (Can the server render all configured templates?)",
    response_class=json_response_class,
)
async def deep_check(request: Request, response: Response) -> List[str]:
    response.status_code = 200
    ret = list()
    for template in list(request.app.state.XDS_TEMPLATES["default"].keys()):
        try:
            req = mock_discovery_request(service_cluster="*")
            await discovery.response(request, req, xds_type=template)
        # pylint: disable=broad-except
        except Exception as e:
            ret.append(f"Failed {template}: {str(e)}")
        else:
            ret.append(f"Rendered {template} OK")
    return ret


@router.get("/version", summary="Display the current version of Sovereign")
async def version_check() -> Response:
    return PlainTextResponse(f"Sovereign {__version__}")
