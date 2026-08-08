from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "software_sales.courses"
    label = "courses"

    def ready(self):
        from . import signals  # noqa: F401
