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
        # First time Loading Page
        if not request.GET.get("allowance-select"):
            print("First Time Load")
            allowance_lst = Allowance.objects.all()
            return render(request, 'main/Show_Allowance.html', {"allowance_lst": allowance_lst})

        else:
            print("Second TIme Load")
            print(request.GET.get("allowance-select"))
            allowance_lst = Allowance.objects.all()
            THIS = Expense.objects.filter(allowance=request.GET.get("allowance-select")).first()
            return render(request, 'main/Show_Allowance.html', {"allowance_lst": allowance_lst, "THIS": THIS})



# Getting Chat Data
def chart_data(request):

    if request.method == "GET":
        #Getting Data
        # data = {
        #     "labels": ["Food", "Rent", "Transport"],
        #     "values": [300, 1000, 150]
        # }

        names_lst = []
        values_lst = []
        for i in Expense.objects.all():
            names_lst.append(i.expense)
            values_lst.append(i.limit)
        data = {
            'labels': names_lst,
            'values': values_lst,
            'color': 'rgb(0 150 255)'
        }

        return JsonResponse(data)

def settings(request):
    return render(request, 'main/Settings.html', {})