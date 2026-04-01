from .base import *

# Add django_browser_reload only in DEBUG mode
INSTALLED_APPS += ["django_browser_reload"]

# Add django_browser_reload middleware only in DEBUG mode
MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# Add for windows user
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"