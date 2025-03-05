from django.shortcuts import render, redirect
from main.models import *
from main.forms import *


# Homepage
def home(request):
    return render(request, 'main/Home.html', {})


# Create New Allowance
def create(request):

    if request.method == "GET":
        # Collecting Forms
        form = AllowanceForm()
        form2 = AllowanceExpenseForm()
        return render(request, 'main/Create_Allowance.html', {"form": form, "form2": form2})

    elif request.method == "POST":
        allowance = request.POST.get("default_allowance")
        expense = request.POST.get('expense')
        expense_limit = request.POST.get('limit')

        new_allowance = Allowance.objects.create(user=request.user, default_allowance=allowance)
        new_expense = Expense.objects.create(allowance=new_allowance, expense=expense, limit=expense_limit)

        new_allowance.save()
        new_expense.save()

        return redirect(home)


def settings(request):
    return render(request, 'main/Settings.html', {})