'''Factory pattern to create flask app'''
from werkzeug.exceptions import HTTPException
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

from app.configs.cache_cfg import CacheConfig
from app.configs.database_cfg import DevConfig
from app.error.handler import base_exc_handler, http_exc_handler
from app.models.database import db
# this import should be in place, to let migrate command find the tables
import app.models.models as models
from app.routes import create_cache_bp, create_health_bp
from app.routes.models import create_crud_blueprint


BASE_PATH = '/api'
bootstrap = Bootstrap()
cache = Cache()
migrate = Migrate()


def create_app() -> Flask:
    '''Create the flask app'''
    app = Flask(__name__)
    app.config.from_object(DevConfig)
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

    app.register_error_handler(HTTPException, http_exc_handler)
    app.register_error_handler(Exception, base_exc_handler)

    routes = [('/', create_health_bp(limiter)),
          (BASE_PATH, create_crud_blueprint(models.Game, cache)),
          (BASE_PATH, create_crud_blueprint(models.Faction, cache)),
          (BASE_PATH, create_crud_blueprint(models.Structure, cache)),
          (BASE_PATH, create_crud_blueprint(models.StructureXFaction, cache)),
          (BASE_PATH, create_crud_blueprint(models.Infantry, cache)),
          (BASE_PATH, create_crud_blueprint(models.InfantryXFaction, cache)),
          (BASE_PATH, create_crud_blueprint(models.Tank, cache)),
          (BASE_PATH, create_crud_blueprint(models.TankXFaction, cache)),
          (BASE_PATH, create_crud_blueprint(models.Boat, cache)),
          (BASE_PATH, create_crud_blueprint(models.BoatXFaction, cache)),
          (BASE_PATH, create_crud_blueprint(models.Plane, cache)),
          (BASE_PATH, create_crud_blueprint(models.PlaneXFaction, cache)),
          (BASE_PATH, create_cache_bp(cache))
          ]

    for url, blueprint in routes:
        app.register_blueprint(blueprint, url_prefix=url)
    return app
