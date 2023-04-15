

from .base import *

DEBUG = True
# ALLOWED_HOSTS = []
INSTALLED_APPS += ["debug_toolbar", "silk"]



MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
# MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")


# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ==============================================================================
# THIRD-PARTY APPS
# ============================================================================== 

SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER':  config('DB_USER'),
        'PASSWORD':  config('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# INTERNAL_IPS = [ "127.0.0.1"]
# # DEBUG_TOOLBAR_CONFIG = {
# #     'JQUERY_URL': '',
# # }
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}