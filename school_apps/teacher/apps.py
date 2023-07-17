from django.apps import AppConfig


class TeachersConfig(AppConfig):
    name = "school_apps.teacher"

    def ready(self):
        import school_apps.teacher.signals
