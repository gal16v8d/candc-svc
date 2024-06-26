"""Init Api to add swagger"""

from flask_restx import Api


api = Api(version="1.0", title="C&C API", description="Command and Conquer Info API")
