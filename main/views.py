from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import *
from main.forms import *


# Homepage
def home(request):
    return render(request, 'main/Home.html', {})


# Create New Allowance
def create(request):
    if request.method == "GET":
        # Collecting Forms
        # Getting Last Used Allowance
        allowance = Allowance.objects.filter(user=request.user).last()

        # Forms
        form = AllowanceForm(instance=allowance)
        form2 = [AllowanceExpenseForm(instance=item) for item in Expense.objects.filter(allowance=allowance)]

        return render(request, 'main/Create_Allowance.html', {"form": form, "form2": form2})

    elif request.method == "POST":
        # Getting Values
        allowance = request.POST.get("default_allowance")
        schedules = request.POST.get('schedules')
        expense = request.POST.getlist('expense')
        expense_limit = request.POST.getlist('limit')

        # Creating Allowance & Saving
        new_allowance = Allowance(user=request.user, schedules=schedules, default_allowance=allowance)
        new_allowance.save()

        # Creating Expenses & Saving
        for exp in zip(expense, expense_limit):
            Expense(allowance=new_allowance, expense=exp[0], limit=exp[1]).save()


        return redirect(home)


# Showing all Allowances
def show(request):
    if request.method == "GET":
        allowance = Allowance.objects.filter(user=request.user).last()
        return render(request, 'main/Show_Allowance.html', {"allowance": allowance})


# Getting Chat Data
def chart_data(request):

    if request.method == "GET":
        allowance = Allowance.objects.filter(user=request.user).last()

        names_lst = []
        values_lst = []
        for i in Expense.objects.filter(allowance=allowance):
            names_lst.append(i.expense)
            values_lst.append(i.limit)
        data = {
            'labels': names_lst,
            'values': values_lst,
            'color': 'rgb(0 150 255)',
            'allowance': int(allowance.default_allowance),
            'schedule': allowance.schedules
        }

        return JsonResponse(data)

def settings(request):
    return render(request, 'main/Settings.html', {})