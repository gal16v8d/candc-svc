"""Index for models routes"""

from app.routes.models.crud import crud_route_ns
from app.routes.models.money import money_ns


__all__ = ["crud_route_ns", "money_ns"]
