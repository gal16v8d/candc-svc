""" Init cache module globally to be used across the app"""

from flask_caching import Cache


app_cache = Cache()
