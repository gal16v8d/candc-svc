'''Factory pattern to create flask app'''
import logging
import os
from werkzeug.exceptions import HTTPException
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flasgger import Swagger
from pydantic import ValidationError
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from app.configs.cache_cfg import CacheConfig
from app.configs.lazy_cfg_loader import LazyImporter
from app.configs.log_cfg import log, LOG_NAME
import app.const as consts
from app.core.app_cache import cache
import app.error.handler as handler
from app.models.database import db
# this import should be in place, to let migrate command find the tables
import app.models.models as models
import app.models.schemas as schemas
from app.routes import cache_bp, create_health_bp
from app.routes.models import create_crud_blueprint, money_bp


BASE_PATH = '/api'
bootstrap = Bootstrap()
migrate = Migrate()
log = logging.getLogger(LOG_NAME)


def create_app() -> Flask:
    '''Create the flask app'''
    app = Flask(__name__)
    if os.getenv(consts.envs.CANDC_ENV) == 'prod':
        db_config = LazyImporter(consts.lazy_load.PROD_DB_MODULE)\
            .get_config_class(consts.lazy_load.PROD_DB_CLASS)
    elif os.getenv(consts.envs.CANDC_ENV) == 'dev':
        db_config = LazyImporter(consts.lazy_load.DEV_DB_MODULE)\
            .get_config_class(consts.lazy_load.DEV_DB_CLASS)
    else:
        db_config = LazyImporter(consts.lazy_load.TEST_DB_MODULE)\
            .get_config_class(consts.lazy_load.TEST_DB_CLASS)
    app.config.from_object(db_config)
    app.config.from_object(CacheConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    cache.init_app(app)
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["30/minute"],
        storage_uri="memory://",
    )
    Swagger(app, template=dict(
        info={
            'title': 'C&C Api',
            'version': '1.0.0',
            'description': 'C&C Wiki using Flask'
        }
    ))

    # Integrate the logger with the Flask app
    app.logger.addHandler(log.handlers[0])

    app.register_error_handler(HTTPException, handler.http_exc_handler)
    app.register_error_handler(ValidationError, handler.val_exc_handler)
    app.register_error_handler(IntegrityError, handler.sqlalchemy_exc_handler)
    app.register_error_handler(Exception, handler.base_exc_handler)

    routes = [('/', create_health_bp(limiter)),
              (BASE_PATH, cache_bp),
              (BASE_PATH, money_bp),
              (BASE_PATH, create_crud_blueprint(models.Boat, schemas.BoatBase,
                                                schemas.BoatList)),
              (BASE_PATH, create_crud_blueprint(models.BoatXFaction, schemas.BoatXFactionBase,
                                                schemas.BoatXFactionList)),
              (BASE_PATH, create_crud_blueprint(models.Faction, schemas.FactionBase,
                                                schemas.FactionList)),
              (BASE_PATH, create_crud_blueprint(models.Game, schemas.GameBase,
                                                schemas.GameList)),
              (BASE_PATH, create_crud_blueprint(models.Infantry, schemas.InfantryBase,
                                                schemas.InfantryList)),
              (BASE_PATH, create_crud_blueprint(models.InfantryXFaction,
                                                schemas.InfantryXFactionBase,
                                                schemas.InfantryXFactionList)),
              (BASE_PATH, create_crud_blueprint(models.Plane, schemas.PlaneBase,
                                                schemas.PlaneList)),
              (BASE_PATH, create_crud_blueprint(models.PlaneXFaction, schemas.PlaneXFactionBase,
                                                schemas.PlaneXFactionList)),
              (BASE_PATH, create_crud_blueprint(models.Structure, schemas.StructureBase,
                                                schemas.StructureList)),
              (BASE_PATH, create_crud_blueprint(models.StructureXFaction,
                                                schemas.StructureXFactionBase,
                                                schemas.StructureXFactionList)),
              (BASE_PATH, create_crud_blueprint(models.Tank, schemas.TankBase,
                                                schemas.TankList)),
              (BASE_PATH, create_crud_blueprint(models.TankXFaction, schemas.TankXFactionBase,
                                                schemas.TankXFactionList))
              ]

    for url, blueprint in routes:
        app.register_blueprint(blueprint, url_prefix=url)

    with app.app_context():
        @event.listens_for(db.engine, "before_cursor_execute")
        def log_query(conn, cursor, statement, parameters, context, executemany):
            log.info("SQL Query: \n%s", statement)
            log.info("SQL Args: \n%s", parameters)

    return app
