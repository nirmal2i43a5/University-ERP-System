from django.forms import ModelForm
from django import forms

from .models import MisSetting
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class SettingForm(ModelForm):
    academic_year = forms.IntegerField(required=False)

    class Meta:
        model = MisSetting
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Row(Column("site_title",
                                               css_class="form-group col-md-4  mb-0"),
                                        Column("phone_no",
                                               css_class="form-group col-md-4  mb-0"),
                                        Column("system_email",
                                               css_class="form-group col-md-4 mb-0"),
                                        css_class="form-row",
                                        ),
                                    Row(Column("address",
                                               css_class="form-group col-md-4  mb-0"),
                                        Column("academic_year",
                                               css_class="form-group col-md-4  mb-0"),
                                        Column("footer",
                                        css_class="form-group col-md-4 mb-0"),
                                        ),
                                    Row(Column("version",
                                               css_class="form-group col-md-4  mb-0"),
                                        Column("logo",
                                               css_class="form-group col-md-4  mb-0"),
                                        ),
                                    Submit("submit",
                                           "Save Settings",
                                           css_class="btn text-bold btn-success"),
                                    )
