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
        form = AllowanceForm(instance=Allowance.objects.filter(user=request.user).first())
        form2 = []
        for i in Expense.objects.all():
            form2.append(AllowanceExpenseForm(instance=i))

        return render(request, 'main/Create_Allowance.html', {"form": form, "form2": form2})

    elif request.method == "POST":
        allowance = request.POST.getlist("default_allowance")
        expense = request.POST.getlist('expense')
        expense_limit = request.POST.getlist('limit')

        lst = zip(expense, expense_limit)
        for i in lst:
            print(i)

        return redirect('home')

        # new_allowance = Allowance.objects.create(user=request.user, default_allowance=allowance)
        # new_expense = Expense.objects.create(allowance=new_allowance, expense=expense, limit=expense_limit)
        #
        # new_allowance.save()
        # new_expense.save()
        #
        # return redirect(home)


# Showing all Allowances
def show(request):
    if request.method == "GET":
        lst = Allowance.objects.all()

        return render(request, 'main/Show_Allowance.html', {"lst": lst})


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
            if i.spending:
                names_lst.append("spending")
                values_lst.append(i.spending)
        data = {
            'labels': names_lst,
            'values': values_lst
        }

        return JsonResponse(data)

def settings(request):
    return render(request, 'main/Settings.html', {})