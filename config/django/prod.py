from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "Pastoral-chu.onrender.com",
    ".onrender.com",
    "localhost",
    "127.0.0.1"
]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}