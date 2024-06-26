"""Index for health route"""

from app.routes.cache import cache_ns
from app.routes.health import health_ns


__all__ = ["cache_ns", "health_ns"]
