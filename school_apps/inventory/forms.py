from django.db.models import fields
from django.db.models.base import Model
from .models import Category, Assets, Item, ProcurementRequest, RepairRequest, Transaction, Vendor
from django.forms import ModelForm
from django import forms

class CategoryCreateForm(ModelForm):
    class Meta:
        model=Category
        fields='__all__'

class AssetsCreateForm(ModelForm):
    class Meta:
        model=Assets
        fields='__all__'

class ItemCreateForm(ModelForm):
    class Meta:
        model=Item
        fields = ['id_no', 'category', 'item_type']

class VendorCreateForm(ModelForm):
    class Meta:
        model=Vendor
        fields='__all__'
    
class ProcurementRequestCreateForm(ModelForm):

    class Meta:
        model=ProcurementRequest
        fields='__all__'
        exclude=['requester','request_date', 'status', 'procurement_personnel', 'finance_personnel', 
                'procurement_date', 'finance_date', 'procurement_comment','finance_comment','goto_branch','remaining',
                'is_complete','acquired']


class TransactionCreateForm(ModelForm):
    request_date = forms.DateField(widget=forms.DateInput(attrs = {'type':'date',}))
    class Meta:
        model=Transaction
        fields='__all__'
        exclude=['is_complete', 'completion_date']

class RepairCreateForm(ModelForm):
    
    class Meta:
        model=RepairRequest
        fields='__all__'
        exclude=['requester','is_complete', 'completion_date','requester_dept', 'requester_branch', 'is_complete', 'request_date',
                'status','finance_date', 'finance_personnel','finance_date','finance_comment']
