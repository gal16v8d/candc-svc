'''Basic health check route'''
from flask import Blueprint, Response, jsonify
from flask_limiter import Limiter


def create_health_bp(limiter: Limiter):
    '''Create the health blueprint'''
    health = Blueprint('health', __name__)

    @health.route('/health', methods=['GET'])
    @limiter.exempt
    def health_check() -> Response:
        '''Return UP if app is running'''
        return jsonify(status = 'UP')

    return health
