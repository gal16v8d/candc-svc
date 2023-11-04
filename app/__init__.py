'''Factory pattern to create flask app'''
from werkzeug.exceptions import HTTPException
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flasgger import Swagger
from app.configs.cache_cfg import CacheConfig
from app.configs.database_cfg import DevConfig
from app.configs.log_cfg import log
from app.core.app_cache import cache
from app.error.handler import base_exc_handler, http_exc_handler
from app.models.database import db
# this import should be in place, to let migrate command find the tables
import app.models.models as models
from app.routes import cache_bp, create_health_bp
from app.routes.models import create_crud_blueprint, money_bp


BASE_PATH = '/api'
bootstrap = Bootstrap()
migrate = Migrate()


def create_app(db_config = DevConfig) -> Flask:
    '''Create the flask app'''
    app = Flask(__name__)
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

    app.register_error_handler(HTTPException, http_exc_handler)
    app.register_error_handler(Exception, base_exc_handler)

    routes = [('/', create_health_bp(limiter)),
              (BASE_PATH, cache_bp),
              (BASE_PATH, money_bp),
              (BASE_PATH, create_crud_blueprint(models.Game)),
              (BASE_PATH, create_crud_blueprint(models.Faction)),
              (BASE_PATH, create_crud_blueprint(models.Structure)),
              (BASE_PATH, create_crud_blueprint(models.StructureXFaction)),
              (BASE_PATH, create_crud_blueprint(models.Infantry)),
              (BASE_PATH, create_crud_blueprint(models.InfantryXFaction)),
              (BASE_PATH, create_crud_blueprint(models.Tank)),
              (BASE_PATH, create_crud_blueprint(models.TankXFaction)),
              (BASE_PATH, create_crud_blueprint(models.Boat)),
              (BASE_PATH, create_crud_blueprint(models.BoatXFaction)),
              (BASE_PATH, create_crud_blueprint(models.Plane)),
              (BASE_PATH, create_crud_blueprint(models.PlaneXFaction))
              ]

    for url, blueprint in routes:
        app.register_blueprint(blueprint, url_prefix=url)

    return app
