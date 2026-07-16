
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("Path(__file__).resolve()", "config.django.dev")

application = get_wsgi_application()
