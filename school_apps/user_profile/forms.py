from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    password_validation,
)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from student_management_app.models import CustomUser, UserRole
from django.contrib.auth.models import Group
from student_management_app.models import Staff
from django.utils.translation import gettext_lazy as _


class UserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        empty_label="Select roles ", queryset=Group.objects.all()
    )

    class Meta:
        model = UserRole
        fields = "__all__"


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": " Enter Username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": " Enter Password",
            }
        )
    )
    # user_type = forms.ModelChoiceField(
    #     empty_label="Select roles ", queryset=Group.objects.all())

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
        )


#   class MessageForm(forms.Form):


class CustomSetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    role = forms.ModelChoiceField(
        empty_label="Select Role For Changing Password",
        label="User Role",
        queryset=Group.objects.all(),
    )
    user = forms.ModelChoiceField(
        empty_label="Select User For Changing Password",
        queryset=CustomUser.objects.all(),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, user_id, commit=True):
        # self.user = super(CustomSetPasswordForm, self)
        print(user_id, "================I am inside form ================")
        password = self.cleaned_data["new_password1"]
        user_id.set_password(password)
        if commit:
            user_id.save()
        return user_id
