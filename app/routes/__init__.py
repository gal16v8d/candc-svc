'''Index for health route'''
from app.routes.cache import create_cache_bp
from app.routes.health import create_health_bp


__all__ = ['create_cache_bp', 'create_health_bp']
