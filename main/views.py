from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import *
from main.forms import *
from decimal import Decimal


# Homepage
def home(request):
    return render(request, 'main/Home.html', {})


# Updating Data
def update(request):
    # Getting Allowance
    allowance = Allowance.objects.all()

    # Resetting Allowance
    for item in allowance:
        item.set_allowance = item.default_allowance
        item.save()

    # Resetting Expenses
    for item in allowance:
        for expense in Expense.objects.filter(allowance=item):
            # Setting Expense
            expense.set = expense.limit - sum([Decimal(item[1]) for item in expense.spending])
            expense.save()

            # Setting Allowance
            item.set_allowance -= sum([Decimal(item[1]) for item in expense.spending])
            item.save()


# Getting Chat Data
def chart_data(request):

    if request.method == "GET":
        allowance = Allowance.objects.filter(user=request.user).last()

        names_lst = []
        values_lst = []
        limits_lst = []
        for i in Expense.objects.filter(allowance=allowance):
            names_lst.append(i.expense)
            values_lst.append(i.set)
            limits_lst.append((i.limit - i.set))
        data = {
            'labels': names_lst,
            'saved': values_lst,
            'spent': limits_lst,
            'color': 'rgb(0 150 255)',
            'allowance': int(allowance.default_allowance),
            'schedule': allowance.schedules
        }

        return JsonResponse(data)

# Getting Transactions Data


# Showing all Allowances
def show(request):
    update(request)
    if request.method == "GET":
        # Getting Allowance
        allowance = Allowance.objects.filter(user=request.user).last()

        # Getting Expense Spent
        expense = Expense.objects.filter(allowance=allowance)

        # Loading Page
        return render(request, 'main/Show_Allowance.html', {"allowance": allowance, "expense": expense})

    elif request.method == "POST":
        # Getting Allowance
        allowance = Allowance.objects.filter(user=request.user).last()

        # Getting Expense
        expense_name = request.POST.get('expense_name')
        expense = Expense.objects.get(allowance=allowance, expense=expense_name)

        # Getting Values
        expense_description = request.POST.get('expense_description')
        expense_amount = request.POST.get('expense_amount')
        # Adding Spending Cost
        expense.add_entry(expense_description, expense_amount)

        return redirect(show)


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


# Settings
def settings(request):
    return render(request, 'main/Settings.html', {})







