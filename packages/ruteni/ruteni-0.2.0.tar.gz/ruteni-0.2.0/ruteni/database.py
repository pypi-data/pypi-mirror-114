# -*- coding: utf-8 -*-

import logging
from databases import Database
from sqlalchemy import MetaData
from starlette.applications import Starlette

from ruteni import configuration

logger = logging.getLogger(__name__)

metadata = MetaData()


async def startup(app: Starlette) -> None:
    DATABASE_URL = configuration.get("RUTENI_DATABASE_URL")
    if configuration.env == "development":
        from sqlalchemy import create_engine

        engine = create_engine(DATABASE_URL)
        # if engine.dialect.name == "sqlite":
        metadata.create_all(engine)

    database = Database(DATABASE_URL)
    await database.connect()
    app.state.database = database
    logger.info("started")


async def shutdown(app: Starlette) -> None:
    if app.state.database:
        await app.state.database.disconnect()
        app.state.database = None
    logger.info("stopped")


configuration.add_service("database", startup, shutdown)

logger.info("loaded")
