'''Factory pattern to create flask app'''
from werkzeug.exceptions import HTTPException
from flask import Flask
from flask_migrate import Migrate

from app.configs.database_cfg import DevConfig
from app.error.handler import base_exc_handler, http_exc_handler
from app.models.database import db
# this import should be in place, to let migrate command find the tables
import app.models.models as models
from app.routes.health import health
from app.routes.models import create_crud_blueprint


BASE_PATH = '/api'
ROUTES = [('/', health),
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
          (BASE_PATH, create_crud_blueprint(models.PlaneXFaction)),
          ]
migrate = Migrate()


def create_app() -> Flask:
    '''Create the flask app'''
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_error_handler(HTTPException, http_exc_handler)
    app.register_error_handler(Exception, base_exc_handler)

    for url, blueprint in ROUTES:
        app.register_blueprint(blueprint, url_prefix=url)
    return app
