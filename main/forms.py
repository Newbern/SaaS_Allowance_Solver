from django import forms
from main.models import *



class AllowanceForm(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = ['default_allowance']
        widgets = {
            'default_allowance': forms.NumberInput(),
        }

class AllowanceExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense', 'limit']
        widgets = {
            'expense': forms.TextInput(),
            'limit': forms.NumberInput(),
        }