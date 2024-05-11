"""Index for health route"""

from app.routes.cache_bp import cache_bp
from app.routes.health import create_health_bp


__all__ = ["cache_bp", "create_health_bp"]
