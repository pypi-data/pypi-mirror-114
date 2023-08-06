# -*- coding: utf-8 -*-

import httpx
import logging
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthCredentials,
    UnauthenticatedUser,
    AuthenticationBackend,
)
from authlib.integrations.starlette_client import OAuth
from authlib.oidc.discovery.well_known import get_well_known_url
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.sql import select
from sqlalchemy_utils import EmailType

from ruteni import configuration
from ruteni.database import metadata
from ruteni.authentication.google import GoogleUser

logger = logging.getLogger(__name__)


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32), nullable=False),
    Column("given_name", String(16), nullable=False),
    Column("family_name", String(16), nullable=False),
    Column("email", EmailType, nullable=False, unique=True),
    Column("locale", String(5), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)

groups = Table(
    "groups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(28), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)

memberships = Table(
    "memberships",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("group_id", Integer, ForeignKey(groups.c.id), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)


class SessionAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request):
        user = request.session.get("user")
        if user:
            if user["iss"] == "https://accounts.google.com":
                profile = {
                    k: user[k]
                    for k in (
                        "id",
                        "email",
                        "name",
                        "given_name",
                        "family_name",
                        "locale",
                        "groups",
                    )
                }
                scopes = user["groups"] + ["authenticated"]
                return AuthCredentials(scopes), GoogleUser(profile)
            else:
                logger.warn(f'unknown issuer {user["iss"]}')

        return AuthCredentials(), UnauthenticatedUser()


issuer = configuration.get("OPENID_ISSUER", default="https://accounts.google.com")
oauth = OAuth(configuration)
oauth.register(
    name="google",
    server_metadata_url=get_well_known_url(issuer, external=True),
    client_kwargs={"scope": "openid email profile"},
)


async def login(request: Request) -> Response:
    redirect_uri = request.url_for("auth")
    try:
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except httpx.ConnectTimeout:
        return PlainTextResponse(
            "Connection timeout redirecting to google. Please retry later."
        )


async def auth(request: Request) -> Response:

    # get the token from the URL and parse it to get the user data
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    # look for the user ID in the database from his/her email address
    query = select([users.c.id]).where(users.c.email == user["email"])
    user_id = await request.app.state.database.fetch_val(query)

    # if the user is unknown, create a new profile
    if user_id is None:
        # @todo insert new user from google information, returning the new ID
        return PlainTextResponse(f'{user["email"]} is not in the database')

    # record the user ID
    user["id"] = user_id

    # look for the groups the user belongs to
    stmt = (
        select([groups.c.name])
        .select_from(groups.join(memberships))
        .where(memberships.c.user_id == user_id)
    )
    rows = await request.app.state.database.fetch_all(stmt)
    user["groups"] = [row[0] for row in rows]

    logger.info(f'{user["email"]} logged in; groups: {user["groups"]}')

    # record in the user data in the session
    request.session["user"] = dict(user)
    return RedirectResponse(url="/")


async def logout(request: Request) -> Response:
    request.session.pop("user", None)
    return RedirectResponse(url="/")


configuration.add_middleware(
    SessionMiddleware,
    secret_key=configuration.get("RUTENI_SESSION_SECRET_KEY", default=""),
    https_only=not configuration.is_devel,
)
configuration.add_middleware(
    AuthenticationMiddleware, backend=SessionAuthenticationBackend()
)

configuration.add_route("/login", login)
configuration.add_route("/auth", auth, name="auth")
configuration.add_route("/logout", logout)

logger.info("loaded")
