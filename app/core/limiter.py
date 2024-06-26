"""Init base props for flask limiter"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app_limiter = Limiter(
    get_remote_address,
    default_limits=["30/minute"],
    storage_uri="memory://",
)
