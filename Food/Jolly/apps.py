# Jolly/apps.py

from django.apps import AppConfig

class JollyConfig(AppConfig):
    # Ensure this matches the module name you use in settings.py
    name = 'Jolly'
    default_auto_field = 'django.db.models.BigAutoField'

    # The crucial fix: This runs ONLY after all apps and models are loaded.
    def ready(self):
        # We use the uppercase 'Jolly' to match your module structure
       # import Jolly.signals
       pass