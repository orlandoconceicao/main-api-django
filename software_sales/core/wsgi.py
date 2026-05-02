import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "software_sales.core.settings")

application = get_wsgi_application()

"software_sales.core.wsgi.application"