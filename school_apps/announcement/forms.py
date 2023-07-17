from django import forms
from school_apps.announcement.models import Notice, Holiday


class DateInput(forms.DateInput):
    input_type = "date"


class NoticeForm(forms.ModelForm):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": " Enter Notice Title",
            }
        ),
    )

    class Meta:
        model = Notice
        fields = (
            "title",
            "file",
        )


class HolidayForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": " Enter Title",
            }
        )
    )
    from_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        )
    )
    to_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        )
    )

    class Meta:
        model = Holiday
        fields = "__all__"
