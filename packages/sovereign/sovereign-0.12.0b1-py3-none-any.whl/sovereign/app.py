import os
import asyncio
import traceback
import uvicorn
from typing import Mapping, Any
from collections import namedtuple
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse, Response, JSONResponse
from pkg_resources import resource_filename
from pydantic.error_wrappers import ValidationError

from sovereign import (
    __version__,
    json_response_class,
    get_request_id,
    config_loader,
)
from sovereign.utils import dictupdate
from sovereign.views import crypto, discovery, healthchecks, admin, interface
from sovereign.middlewares import (
    RequestContextLogMiddleware,
    LoggingMiddleware,
    ScheduledTasksMiddleware,
)
from sovereign.schemas import (
    SovereignAsgiConfig,
    SovereignConfig,
    SovereignConfigv2,
)
from sovereign.logs import LoggerBootstrapper
from sovereign.statistics import configure_statsd
from sovereign.sources import SourcePoller
from sovereign.context import TemplateContext
from sovereign.utils.crypto import create_cipher_suite

Router = namedtuple("Router", "module tags prefix")

CONFIG_PATH = os.getenv("SOVEREIGN_CONFIG", "file:///etc/sovereign.yaml")

try:
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    SENTRY_INSTALLED = True
except ImportError:  # pragma: no cover
    SENTRY_INSTALLED = False


async def parse_raw_configuration(path: str) -> Mapping[Any, Any]:
    ret: Mapping[Any, Any] = dict()
    for p in path.split(","):
        spec = config_loader.Loadable.from_legacy_fmt(p)
        ret = dictupdate.merge(obj_a=ret, obj_b=await spec.load(), merge_lists=True)  # type: ignore
    return ret


def generic_error_response(r: Request, e: Exception) -> JSONResponse:
    """
    Responds with a JSON object containing basic context
    about the exception passed in to this function.

    If the server is in debug mode, it will include a traceback in the response.

    The traceback is **always** emitted in logs.
    """
    tb = [line for line in traceback.format_exc().split("\n")]
    error = {
        "error": e.__class__.__name__,
        "detail": getattr(e, "detail", "-"),
        "request_id": get_request_id(),
    }
    r.app.state.LOGGER.queue_log_fields(
        ERROR=error["error"],
        ERROR_DETAIL=error["detail"],
        TRACEBACK=tb,
    )
    # Don't expose tracebacks in responses, but add it to the logs
    if r.app.state.DEBUG:
        error["traceback"] = tb
    return json_response_class(
        content=error, status_code=getattr(e, "status_code", 500)
    )


def init_app() -> FastAPI:
    application: FastAPI = FastAPI(title="Sovereign", version=__version__)

    application.state.CONFIG = dict()

    routers = (
        Router(discovery.router, ["Configuration Discovery"], ""),
        Router(crypto.router, ["Cryptographic Utilities"], "/crypto"),
        Router(admin.router, ["Debugging Endpoints"], "/admin"),
        Router(interface.router, ["User Interface"], "/ui"),
        Router(healthchecks.router, ["Healthchecks"], ""),
    )
    for router in routers:
        application.include_router(
            router.module, tags=router.tags, prefix=router.prefix
        )

    application.add_middleware(RequestContextLogMiddleware)
    application.add_middleware(LoggingMiddleware)
    application.add_middleware(ScheduledTasksMiddleware)

    @application.exception_handler(500)
    async def exception_handler(r: Request, exc: Exception) -> JSONResponse:
        """
        We cannot incur the execution of this function from unit tests
        because the starlette test client simply returns exceptions and does
        not run them through the exception handler.
        Ergo, this is a facade function for `generic_error_response`
        """
        return generic_error_response(r, exc)  # pragma: no cover

    @application.get("/")
    async def redirect_to_docs() -> Response:
        return RedirectResponse("/ui")

    @application.get("/static/{filename}", summary="Return a static asset")
    async def static(filename: str) -> Response:
        return FileResponse(resource_filename("sovereign", f"static/{filename}"))

    @application.on_event("startup")
    async def initialize_configuration() -> None:
        parsed_config = await parse_raw_configuration(CONFIG_PATH)
        try:
            config = SovereignConfigv2(**parsed_config)
        except ValidationError:
            old_config = SovereignConfig(**parsed_config)
            config = SovereignConfigv2.from_legacy_config(old_config)

        s = application.state
        s.CONFIG = config
        s.DEBUG = config.debug
        s.XDS_TEMPLATES = config.xds_templates()
        s.LOGGER = LoggerBootstrapper(config)
        s.STATS = configure_statsd(config=config.statsd)
        s.ENCRYPTION_KEY = (
            config.authentication.encryption_key.get_secret_value().encode()
        )
        s.CIPHER_SUITE = create_cipher_suite(key=s.ENCRYPTION_KEY, logger=s.LOGGER)
        s.POLLER = SourcePoller(
            sources=config.sources,
            matching_enabled=config.matching.enabled,
            node_match_key=config.matching.node_key,
            source_match_key=config.matching.source_key,
            source_refresh_rate=config.source_config.refresh_rate,
            logger=s.LOGGER.application_log,
            stats=s.STATS,
        )
        s.TEMPLATE_CONTEXT = TemplateContext(
            refresh_rate=config.template_context.refresh_rate,
            configured_context=config.template_context.context,
            poller=s.POLLER,
            encryption_suite=s.CIPHER_SUITE,
            disabled_suite=create_cipher_suite(b"", s.LOGGER),
        )

        s.SENTRY_DSN = config.sentry_dsn.get_secret_value()
        if SENTRY_INSTALLED and s.SENTRY_DSN:
            sentry_sdk.init(s.SENTRY_DSN)
            application.add_middleware(SentryAsgiMiddleware)
            s.LOGGER.application_log(event="Sentry middleware enabled")

    @application.on_event("startup")
    async def start_poller() -> None:
        s = application.state
        s.POLLER.lazy_load_modifiers(s.CONFIG.modifiers)
        s.POLLER.lazy_load_global_modifiers(s.CONFIG.global_modifiers)

    @application.on_event("startup")
    async def keep_sources_uptodate() -> None:
        asyncio.create_task(application.state.POLLER.poll_forever())

    @application.on_event("startup")
    async def refresh_template_context() -> None:
        asyncio.create_task(application.state.TEMPLATE_CONTEXT.refresh_context())

    @application.on_event("startup")
    async def log_startup() -> None:
        application.state.LOGGER.application_log(
            event=f"Sovereign started and listening on {asgi_config.host}:{asgi_config.port}"
        )

    return application


app = init_app()
asgi_config = SovereignAsgiConfig()


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
