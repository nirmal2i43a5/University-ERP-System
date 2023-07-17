from django.urls import path
from .views import GeneralSettingCreate, GeneralSettingUpdate

app_name = "setting_app"

urlpatterns = [
    # path('add_setting/',GeneralSettingCreate.as_view(), name = 'add_setting'),
    path("general_setting/", GeneralSettingUpdate, name="general_setting"),
]
