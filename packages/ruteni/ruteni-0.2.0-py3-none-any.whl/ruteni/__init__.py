# -*- coding: utf-8 -*-

import os
import logging
import socketio
from typing import Callable, List, Sequence, Union
from starlette.config import Config
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.authentication import requires


# @todo https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/
# logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Api:
    """
    Manage a web API
    """

    def __init__(
        self,
        app: Starlette,
        name: str,
        version: int,
        *,
        scopes: Union[str, Sequence[str]] = None,
        status_code: int = 403,
        redirect: str = None,
    ) -> None:
        self.app = app
        self.shield = (
            None if scopes is None else requires(scopes, status_code, redirect)
        )

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
    ) -> None:
        func = endpoint if self.shield is None else self.shield(endpoint)
        self.app.add_route(
            path,
            func,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )


class Configuration(Config):
    def __init__(self) -> None:
        super().__init__(os.environ.get("RUTENI_CONFIG", ".env"))
        self.starlette = dict(
            routes=[],
            middleware=[],
            on_startup=[],
            on_shutdown=[],
        )
        self.socketio = {}
        self.asgi = {}
        self.services = []

    @property
    def is_devel(self):
        return self.env == "development"

    @property
    def is_debug(self):
        return self.get("RUTENI_DEBUG", cast=bool, default=False)

    @property
    def env(self):
        return self.get("RUTENI_ENV", default="production")

    def add_service(self, name, startup, shutdown):
        self.services.append((name, startup, shutdown))

    def create_public_api(self, name: str, version: int) -> Api:
        return Api(self, name, version)

    def create_protected_api(
        self,
        name: str,
        version: int,
        scopes: Union[str, Sequence[str]],
        *,
        status_code: int = 403,
        redirect: str = None,
    ) -> Api:
        return Api(
            self,
            name,
            version,
            scopes=scopes,
            status_code=status_code,
            redirect=redirect,
        )

    def add_middleware(self, *args, **kwargs) -> None:
        self.starlette["middleware"].append(Middleware(*args, **kwargs))

    def add_route(self, *args, **kwargs) -> None:
        self.starlette["routes"].append(Route(*args, **kwargs))

    def add_mount(self, *args, **kwargs) -> None:
        self.starlette["routes"].append(Mount(*args, **kwargs))

    def add_static(self, path, directory):
        self.add_mount(path, app=StaticFiles(directory=directory))

    def add_event_handler(self, event_type: str, func: Callable) -> None:
        assert event_type in ("startup", "shutdown")
        if event_type == "startup":
            self.starlette["on_startup"].append(func)
        else:
            self.starlette["on_shutdown"].append(func)


configuration = Configuration()


class Ruteni(socketio.ASGIApp):
    def __init__(self) -> None:
        configuration.add_event_handler("startup", self._start_services)
        configuration.add_event_handler("shutdown", self._stop_services)
        super().__init__(
            socketio.AsyncServer(async_mode="asgi", **configuration.socketio),
            Starlette(debug=configuration.is_debug, **configuration.starlette),
            **configuration.asgi,
        )
        self.other_asgi_app.state.sio = self.engineio_server
        self.shutdown_callbacks = []

    async def _start_services(self) -> None:
        try:
            for name, startup, shutdown in configuration.services:
                await startup(self.other_asgi_app)
                self.shutdown_callbacks.append((name, shutdown))
        except:
            logger.exception("start")
            await self._stop_services()
            raise

    async def _stop_services(self) -> None:
        while len(self.shutdown_callbacks):
            name, shutdown = self.shutdown_callbacks.pop()
            try:
                await shutdown(self.other_asgi_app)
            except:
                logger.exception("stop")
