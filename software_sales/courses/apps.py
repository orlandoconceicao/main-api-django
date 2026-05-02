from django.apps import AppConfig

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'software_sales.core'

    def ready(self):
        import software_sales.courses.signals