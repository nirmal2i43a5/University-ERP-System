from django import forms
from django.forms import ModelForm, inlineformset_factory
from school_apps.library.models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = BookEntry
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))


class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(widget=forms.Select(attrs={}),
    queryset = Category.objects.all())

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}),
        }

class BookAddForm(forms.ModelForm):
    class Meta:
        model = BookEntry
        exclude = ('price','language',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Book Title', 'id': 'title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Author Name','id': 'author'}),
            'isbn': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Book ISBN', 'id': 'isbn'}),
            'language': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Language of the book', 'id': 'language'}),
            'category': forms.Select(attrs={'class': 'form-control','placeholder':'Select Category', 'id': 'category'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Book QUantity', 'id': 'quantity'}),
            # 'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Enter Book Price','id': 'price'}),
        }

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'

class BookIssueForm(ModelForm):
  
    class Meta:
        model=BookIssue
        # fields = '__all__'
        exclude = ['isbn','expirydate']
       

class BookIssueEditForm(ModelForm):
    class Meta:
        model=BookIssue
        # fields = '__all__'
        exclude = ['isbn','expirydate','issue_id']
        
# BookIssueFormset=inlineformset_factory(Issue, BookIssue, form=BookIssueForm,extra=1)

class BookReturnForm(ModelForm):
    class Meta:
        model = BookReturn
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book_issue'].disabled = True

# BookIssueReturnFormset=inlineformset_factory(Issue, BookReturn, form=BookReturnForm,extra=1)


class AddMemberForm(forms.ModelForm):
    # user_type = forms.ModelChoiceField(
    #     empty_label="Select User Type ", queryset=Group.objects.exclude(name__in = ['Parent','Super-Admin','Bachelor-Admin','Master-Admin','Admin']))
    
    class Meta:
        model = LibraryMemberProfile
        exclude = ('library_card_no',)


class EditMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMemberProfile
        fields = '__all__'
        exclude = ('user','member',)
    # full_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'id': 'full_name',
    #     'data-val': 'true',
    #     'data-val-required': 'Please enter first name',
    # }))
    # email = forms.CharField(widget=forms.EmailInput(attrs={
    #     'class': 'form-control',
    #     'id': 'email',
    #     'data-val': 'true',
    #     'data-val-required': 'Please enter email',
    # }))
    # avatar = forms.ImageField(widget=forms. FileInput(attrs={
    #     'class': 'form-control',
    #     'id': 'email',
    #     'data-val': 'true',
    #     'data-val-required': 'Please enter email',
    # }))

class MemberDetailForm(forms.ModelForm):
    class Meta:
        model = LibraryMemberProfile
        fields = '__all__'
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'first_name',
        'data-val': 'true',
        'data-val-required': 'Please enter first name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'last_name',
        'data-val': 'true',
        'data-val-required': 'Please enter last name',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    avatar = forms.ImageField(widget=forms. FileInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    
class BookRenewForm(forms.ModelForm):
    class Meta:
        model = BookRenew
        exclude = ('expirydate',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book_issue'].disabled = True
        self.fields['member_id'].disabled = True
