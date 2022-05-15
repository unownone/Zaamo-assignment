from django.apps import AppConfig


class VideoapiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "videoapi"

    def ready(self):
        from videoapi.updater import start

        start()
