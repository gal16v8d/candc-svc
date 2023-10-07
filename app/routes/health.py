'''Basic health check route'''
from flask import Blueprint, Response, jsonify


health = Blueprint('health', __name__)


@health.route('/health', methods=['GET'])
def health_check() -> Response:
    '''Return UP if app is running'''
    return jsonify(status = 'UP')
