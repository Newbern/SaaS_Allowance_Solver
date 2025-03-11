from django import forms
from main.models import *



class AllowanceForm(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = ['default_allowance']
        labels = {'default_allowance': ""}
        widgets = {
            'default_allowance': forms.NumberInput(attrs={'class': 'layouts'}),
        }

class AllowanceExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense', 'limit']
        labels = {'expense': "", 'limit': ""}
        widgets = {
            'expense': forms.TextInput(attrs={'class': 'expense-layouts'}),
            'limit': forms.NumberInput(attrs={'class': 'expense-layouts'}),
        }