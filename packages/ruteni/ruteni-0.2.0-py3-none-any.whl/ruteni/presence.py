# -*- coding: utf-8 -*-

import json
import logging
import itsdangerous
from base64 import b64decode
from starlette.applications import Starlette
from starlette.requests import cookie_parser
from itsdangerous.exc import BadTimeSignature, SignatureExpired
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy_utils import IPAddressType

from ruteni import configuration
from ruteni.database import metadata
from ruteni.authentication import users

logger = logging.getLogger(__name__)

connections = Table(
    "connections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sid", String(28), nullable=False),
    Column("ip_address", IPAddressType, nullable=False),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)


class RuteniPresence:
    def __init__(self, max_age=14 * 24 * 60 * 60):
        # @todo use `signer` and `max_age` from starlette session middleware
        secret_key = configuration.get("RUTENI_SESSION_SECRET_KEY", default="")
        self.signer = itsdangerous.TimestampSigner(secret_key)
        self.max_age = max_age

    def get_user(self, environ):
        if "HTTP_COOKIE" not in environ:
            return None

        cookies = cookie_parser(environ["HTTP_COOKIE"])

        if "session" not in cookies:
            return None

        try:
            data = self.signer.unsign(cookies["session"], max_age=self.max_age)
        except (BadTimeSignature, SignatureExpired):
            return None

        session = json.loads(b64decode(data))

        if "user" not in session:
            return None

        return session["user"]

    async def connect(self, sid: str, environ: dict) -> None:
        # async with self.app.state.sio.eio.session(sid) as session:
        #     session["username"] = username

        # get the current user
        user = self.get_user(environ)
        if user is None:
            return False  # reject connection

        query = connections.insert().values(
            sid=sid, user_id=user["id"], ip_address=environ["REMOTE_ADDR"]
        )
        await self.app.state.database.execute(query)
        logger.info(f"{user['name']} is connected")

    async def disconnect(self, sid: str) -> None:
        query = (
            connections.update()
            .where(connections.c.sid == sid)
            .values(disabled_at=func.now())
        )
        await self.app.state.database.execute(query)
        logger.info(f"{sid}.disconnect+update")

    async def startup(self, app: Starlette) -> None:
        app.state.sio.on("connect", self.connect)
        app.state.sio.on("disconnect", self.disconnect)
        self.app = app
        logger.info("started")

    async def shutdown(self, app: Starlette) -> None:
        # @todo unsubscribe if possible one day
        self.app = None
        logger.info("stopped")


presence = RuteniPresence()
configuration.add_service("presence", presence.startup, presence.shutdown)

logger.info("loaded")
