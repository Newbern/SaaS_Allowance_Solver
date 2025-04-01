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


# class AllowanceExpenseForm(forms.ModelForm):
#     expense = forms.CharField(widget=forms.TextInput(attrs={'class': 'expense-layouts'}), label="")
#     limit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'expense-layouts'}), label="", decimal_places=2)

class AllowanceExpenseForm(forms.ModelForm):
    expense = forms.CharField(widget=forms.TextInput(attrs={'class': 'expense-layouts'}), label="")
    limit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'expense-layouts'}), label="", decimal_places=2)

    class Meta:
        model = Expense
        fields = ['expense', 'limit']

    def __init__(self, *args, data=None, **kwargs):
        super(AllowanceExpenseForm, self).__init__(*args, **kwargs)

        if data:
            self.fields['expense'].initial = data['name']
            self.fields['limit'].initial = data['limit']








