import os
from contextvars import ContextVar
from typing import Type
from pkg_resources import get_distribution, resource_filename

from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates


json_response_class: Type[JSONResponse] = JSONResponse
try:
    import orjson
    from fastapi.responses import ORJSONResponse

    json_response_class = ORJSONResponse
except ImportError:
    try:
        import ujson
        from fastapi.responses import UJSONResponse

        json_response_class = UJSONResponse
    except ImportError:
        pass


_request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    return _request_id_ctx_var.get()


__version__ = get_distribution("sovereign").version
config_path = os.getenv("SOVEREIGN_CONFIG", "file:///etc/sovereign.yaml")
html_templates = Jinja2Templates(resource_filename("sovereign", "templates"))
