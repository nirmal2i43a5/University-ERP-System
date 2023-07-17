from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from student_management_app.models import CustomUser
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    Submit,
    Button,
    HTML,
    Hidden,
    Div,
    Field,
)
from crispy_forms.helper import FormHelper


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            "groups",
            "user_permissions",
            "is_superuser",
            "is_staff",
            "is_active",
        ]
        widgets = {
            "user_permissions": FilteredSelectMultiple(
                "Permission", False, attrs={
                    "rows": "2"}), "groups": FilteredSelectMultiple(
                "Group", False, attrs={
                    "rows": "2"}), }
