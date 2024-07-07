"""Factory pattern to create flask app"""

import logging
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from pydantic import ValidationError
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app.configs.cache_cfg import CacheConfig
from app.configs.lazy_cfg_loader import LazyImporter
from app.configs.log_cfg import log, LOG_NAME
import app.const as consts
from app.core.api import api
from app.core.cache import app_cache
from app.core.limiter import app_limiter
from app.error import handler_api
from app.models.database import db

# this import should be in place, to let migrate command find the tables
from app.models import models, schemas
from app.routes import cache_ns, health_ns
from app.routes.models import crud_route_ns, money_ns


BASE_PATH = "/api"
bootstrap = Bootstrap()
migrate = Migrate()
log = logging.getLogger(LOG_NAME)


def create_app() -> Flask:
    """Create the flask app"""
    app = Flask(__name__)
    if os.getenv(consts.envs.CANDC_ENV) == "prod":
        db_config = LazyImporter(consts.lazy_load.PROD_DB_MODULE).get_config_class(
            consts.lazy_load.PROD_DB_CLASS
        )
    elif os.getenv(consts.envs.CANDC_ENV) == "dev":
        db_config = LazyImporter(consts.lazy_load.DEV_DB_MODULE).get_config_class(
            consts.lazy_load.DEV_DB_CLASS
        )
    else:
        db_config = LazyImporter(consts.lazy_load.TEST_DB_MODULE).get_config_class(
            consts.lazy_load.TEST_DB_CLASS
        )
    app.config.from_object(db_config)
    app.config.from_object(CacheConfig)
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    app_cache.init_app(app)
    app_limiter.init_app(app)

    # Integrate the logger with the Flask app
    app.logger.addHandler(log.handlers[0])

    api.error_handlers[HTTPException] = handler_api.http_exc_handler
    api.error_handlers[ValidationError] = handler_api.val_exc_handler
    api.error_handlers[IntegrityError] = handler_api.sqlalchemy_exc_handler
    api.error_handlers[Exception] = handler_api.base_exc_handler

    api_routes = [
        {
            "name": "boats",
            "model": models.Boat,
            "schema": schemas.BoatBase,
            "schema_list": schemas.BoatList,
        },
        {
            "name": "boatxfactions",
            "model": models.BoatXFaction,
            "schema": schemas.BoatXFactionBase,
            "schema_list": schemas.BoatXFactionList,
        },
        {
            "name": "factions",
            "model": models.Faction,
            "schema": schemas.FactionBase,
            "schema_list": schemas.FactionList,
        },
        {
            "name": "games",
            "model": models.Game,
            "schema": schemas.GameBase,
            "schema_list": schemas.GameList,
        },
        {
            "name": "infantry",
            "model": models.Infantry,
            "schema": schemas.InfantryBase,
            "schema_list": schemas.InfantryList,
        },
        {
            "name": "infantryxfactions",
            "model": models.InfantryXFaction,
            "schema": schemas.InfantryXFactionBase,
            "schema_list": schemas.InfantryXFactionList,
        },
        {
            "name": "planes",
            "model": models.Plane,
            "schema": schemas.PlaneBase,
            "schema_list": schemas.PlaneList,
        },
        {
            "name": "planexfactions",
            "model": models.PlaneXFaction,
            "schema": schemas.PlaneXFactionBase,
            "schema_list": schemas.PlaneXFactionList,
        },
        {
            "name": "structures",
            "model": models.Structure,
            "schema": schemas.StructureBase,
            "schema_list": schemas.StructureList,
        },
        {
            "name": "structurexfactions",
            "model": models.StructureXFaction,
            "schema": schemas.StructureXFactionBase,
            "schema_list": schemas.StructureXFactionList,
        },
        {
            "name": "tanks",
            "model": models.Tank,
            "schema": schemas.TankBase,
            "schema_list": schemas.TankList,
        },
        {
            "name": "tankxfactions",
            "model": models.TankXFaction,
            "schema": schemas.TankXFactionBase,
            "schema_list": schemas.TankXFactionList,
        },
    ]

    namespaces = [cache_ns, health_ns, money_ns]
    namespaces.extend(crud_route_ns(api_routes))

    for ns in namespaces:
        api.add_namespace(ns)

    with app.app_context():

        @event.listens_for(db.engine, "before_cursor_execute")
        def log_query(
            conn, cursor, statement, parameters, context, executemany
        ) -> None:
            log.info("SQL Query: \n%s", statement)
            log.info("SQL Args: \n%s", parameters)

    return app
