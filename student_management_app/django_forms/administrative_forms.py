from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django.contrib.auth.models import Group
from student_management_app.models import (
    StudentGroup,
    Complain,
    SocialLink,
    CertificateTemplate,
    AdminUser,
)


class GroupForm(forms.ModelForm):
    name = forms.CharField(
        label="Number of Vehicle",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Group Name",
            }
        ),
    )

    class Meta:
        model = StudentGroup
        fields = "__all__"


class ComplainForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": " Enter Complain Title",
            }
        )
    )
    role = forms.ModelChoiceField(
        empty_label="Select Role",
        label="User Role",
        queryset=Group.objects.all())

    class Meta:
        model = Complain
        fields = "__all__"


class SocialLinkForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        empty_label="Select Role",
        label="User Role",
        queryset=Group.objects.all())
    facebook = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": " User Facebook Link",
            }
        ),
    )
    twitter = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "User Twitter Link",
            }
        ),
    )
    linkedin = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "User Linkedin Link",
            }
        ),
    )
    google_plus = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "User Google Plus Link",
            }
        ),
    )

    class Meta:
        model = SocialLink
        fields = "__all__"


class CertificateTemplateForm(forms.ModelForm):
    date_of_issue = forms.DateField(
        label="Date Of Issue",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    class Meta:
        model = CertificateTemplate
        fields = (
            "salutations",
            "student",
            "passed_year",
            "certificate_number",
            "date_of_issue",
        )

    def __init__(self, *args, **kwargs):
        super(CertificateTemplateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Row(Column("salutations",
                                               css_class="form-group col-md-6 mb-0"),
                                        Column("student",
                                               css_class="form-group col-md-6 mb-0"),
                                        css_class="form-row",
                                        ),
                                    Row(Column("passed_year",
                                               css_class="form-group col-md-6 mb-0"),
                                        Column("certificate_number",
                                        css_class="form-group col-md-6 mb-0"),
                                        css_class="form-row",
                                        ),
                                    Row(Column("date_of_issue",
                                               css_class="form-group col-md-6 mb-0"),
                                        css_class="form-row",
                                        ),
                                    Row(HTML('<a class="btn btn-danger" href="{% url "certificate:manage_certificate_template" %}">Back</a>'),
                                        HTML('<button class="btn btn-success ml-2" name = "admin_submit" type="submit">Save</button>&nbsp;'),
                                        ),
                                    )


class SystemAdminForm(forms.ModelForm):
    dob = forms.DateField(
        required=False,
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    join_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    contact = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": " Enter Mobile Number",
            }
        ),
    )
    religion = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": " Enter Your Religion",
            }
        ),
    )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": " Enter Address",
            }
        ),
    )

    class Meta:
        model = AdminUser
        fields = "__all__"
        exclude = (
            "admin_user",
            "status",
        )

    def __init__(self, *args, **kwargs):
        super(SystemAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # form_id and form_tag is the main to work with two form
        self.helper.form_method = "post"
        self.helper.form_tag = (
            False  # for two forms   (solve controversy for two forms)
        )

        self.helper.layout = Layout(
            Row(
                # Column('full_name', css_class='form-group col-md-6 mb-0'),
                Column("dob", css_class="form-group col-md-6 mb-0"),
                Column("gender", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("religion", css_class="form-group col-md-6 mb-0"),
                Column("address", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("contact", css_class="form-group col-md-6 mb-0"),
                Column("join_date", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("image", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                HTML(
                    '<a class="btn btn-danger" href="{% url "dashboard" %}">Back</a>'),
                HTML(
                    '<button class="btn btn-success ml-2" name = "admin_submit" type="submit">Save</button>&nbsp;'
                ),
            ),
        )
