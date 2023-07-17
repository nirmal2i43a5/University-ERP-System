from django.apps import AppConfig
from django.db.models.signals import post_migrate


class StudentManagementAppConfig(AppConfig):
    name = "student_management_app"

    def ready(self):
        import student_management_app.signals  # --form normal signal use

        # ---------------using this way assists to create group directly withou
        from .signals import populate_models

        post_migrate.connect(populate_models, sender=self)
