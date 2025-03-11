from django import forms
from main.models import *



class AllowanceForm(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = ['default_allowance', 'schedules']
        labels = {'default_allowance': "", 'schedules': ""}
        widgets = {
            'default_allowance': forms.NumberInput(attrs={'class': 'allowance-layouts'}),
            'schedules': forms.Select(attrs={'class': 'allowance-layouts'}),
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